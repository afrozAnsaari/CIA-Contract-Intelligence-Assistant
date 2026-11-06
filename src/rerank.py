"""Second-stage reranking of BM25 candidates (optional; `reranker.enabled`, default off).

Stage 1 (unchanged): BM25 ranks the chunks of the routed contract (or the explicit document
filter). Stage 2 (this module): the top `reranker.candidate_k` of those chunks are re-scored by a
cross-encoder that reads (question, chunk text) pairs jointly; the remaining chunks keep their
BM25 order after the reranked head. Passage selection (overlap policy) then runs on the new order.

Guarantees:
  - Only ORDER changes. Chunk ids, document ids, offsets and text are never modified; the
    BM25 score stays in `Passage.score`, the cross-encoder score is stored separately.
  - Reranking never adds or removes candidates, so the document filter / routing mask holds.
  - Ties on the reranker score keep BM25 order (stable sort on (-rerank_score, bm25_rank)).
  - Duplicate chunk ids in the input are scored once; later duplicates are dropped.
  - Empty candidate lists never touch (or load) the model.
  - Failures raise RerankError; a failed reranking is never reported as a successful one.
  - The model is loaded lazily on first use, never at import time.
  - Abstention signals are computed by BM25 before this stage and are not changed by it.

Model: cross-encoder/ms-marco-MiniLM-L-6-v2 (Apache-2.0, ~22.7M parameters, ~87 MB safetensors),
trained on MS MARCO web passage ranking, i.e. NOT on legal text. Needs the optional `dense` extra
(`uv sync --extra dense`) and one download from the Hugging Face Hub; afterwards set
`reranker.local_files_only: true` (or HF_HUB_OFFLINE=1) to run offline.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Protocol, Sequence


class RerankError(RuntimeError):
    """Model loading or inference failed; reranking did not happen."""


class Scorer(Protocol):
    def score(self, query: str, texts: Sequence[str], batch_size: int) -> list[float]: ...


class CrossEncoderScorer:
    """sentence-transformers CrossEncoder, loaded on first `score` call."""

    def __init__(self, model_name: str, device: str = "cpu", max_length: int | None = 512,
                 local_files_only: bool = False):
        self.model_name, self.device = model_name, device
        self.max_length, self.local_files_only = max_length, local_files_only
        self._model = None
        self.load_seconds: float | None = None
        self.n_parameters: int | None = None

    def _load(self):
        if self._model is not None:
            return self._model
        t0 = time.perf_counter()
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as e:
            raise RerankError("Cross-encoder reranking needs the optional extra: uv sync --extra dense") from e
        try:
            self._model = CrossEncoder(self.model_name, device=self.device, max_length=self.max_length,
                                       local_files_only=self.local_files_only)
        except Exception as e:  # network, missing files, bad name, bad device ...
            hint = (" (local_files_only is on: download the model once with it off, or unset HF_HUB_OFFLINE)"
                    if self.local_files_only else "")
            raise RerankError(f"Could not load cross-encoder {self.model_name!r} on {self.device!r}: "
                              f"{type(e).__name__}: {e}{hint}") from e
        self.load_seconds = time.perf_counter() - t0
        try:
            self.n_parameters = int(sum(p.numel() for p in self._model.model.parameters()))
        except Exception:  # pragma: no cover - informational only
            self.n_parameters = None
        return self._model

    def score(self, query: str, texts: Sequence[str], batch_size: int) -> list[float]:
        model = self._load()
        try:
            out = model.predict([(query, t) for t in texts], batch_size=batch_size,
                                show_progress_bar=False, convert_to_numpy=True)
        except Exception as e:
            raise RerankError(f"Cross-encoder inference failed: {type(e).__name__}: {e}") from e
        return [float(x) for x in list(out.reshape(-1))]


@dataclass
class RerankResult:
    order: list[int]  # chunk ids: reranked head followed by the untouched BM25 tail
    scores: dict[int, float]  # chunk id -> reranker score (head only)
    bm25_rank: dict[int, int]  # chunk id -> 1-based rank in the BM25 order
    n_reranked: int = 0
    seconds: float = 0.0
    timings: dict = field(default_factory=dict)


class Reranker:
    def __init__(self, scorer: Scorer, candidate_k: int = 50, batch_size: int = 16):
        if int(candidate_k) < 1 or int(batch_size) < 1:
            raise ValueError("reranker.candidate_k and reranker.batch_size must be >= 1")
        self.scorer, self.candidate_k, self.batch_size = scorer, int(candidate_k), int(batch_size)

    def rerank(self, query: str, ranked: Sequence[int], text_of) -> RerankResult:
        """Rerank the first `candidate_k` unique ids of `ranked`; `text_of(id)` gives the text."""
        unique = list(dict.fromkeys(int(i) for i in ranked))  # dedupe, keep BM25 order
        bm25_rank = {cid: r for r, cid in enumerate(unique, start=1)}
        head, tail = unique[: self.candidate_k], unique[self.candidate_k:]
        if not head:
            return RerankResult(order=[], scores={}, bm25_rank={})
        t0 = time.perf_counter()
        raw = self.scorer.score(query, [text_of(i) for i in head], self.batch_size)
        dt = time.perf_counter() - t0
        if len(raw) != len(head):
            raise RerankError(f"Reranker returned {len(raw)} scores for {len(head)} candidates")
        if any(not isinstance(s, (int, float)) or math.isnan(s) for s in raw):
            raise RerankError("Reranker returned a non-numeric or NaN score")
        scores = {cid: float(s) for cid, s in zip(head, raw)}
        new_head = sorted(head, key=lambda c: (-scores[c], bm25_rank[c]))
        return RerankResult(order=new_head + tail, scores=scores, bm25_rank=bm25_rank,
                            n_reranked=len(head), seconds=dt)


def build_reranker(rcfg: dict, scorer: Scorer | None = None) -> Reranker | None:
    """Reranker from the `reranker` config section, or None when disabled."""
    if not rcfg or not rcfg.get("enabled"):
        return None
    if scorer is None:
        if rcfg["backend"] != "cross_encoder":
            raise ValueError(f"Unknown reranker.backend {rcfg['backend']!r}")
        scorer = CrossEncoderScorer(rcfg["model_name"], device=rcfg["device"], max_length=rcfg.get("max_length"),
                                    local_files_only=bool(rcfg.get("local_files_only", False)))
    return Reranker(scorer, rcfg["candidate_k"], rcfg["batch_size"])
