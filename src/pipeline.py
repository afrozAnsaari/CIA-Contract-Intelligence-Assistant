"""The single query pipeline shared by the CLI, the Streamlit app and evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .abstention import decide
from .config import load_config, resolve_path
from .data import load_documents, load_mini_tests, referenced_documents
from .rerank import RerankError, Scorer
from .verify import Generator, apply_verification, build_verifier
from .retrieval import Index, RetrievalOutput

DISCLAIMER = ("Retrieval aid only - not legal advice. Passages are verbatim excerpts with source "
              "offsets; verify against the full contract.")


class PipelineError(RuntimeError):
    """User-facing error (missing data/index, bad input)."""


@dataclass
class SearchResult:
    query: str
    abstained: bool
    abstention_reason: str
    signal: str
    signal_value: float | None
    threshold: float
    passages: list[dict] = field(default_factory=list)
    config_name: str = ""
    doc_signal_value: float | None = None
    doc_threshold: float | None = None
    document_filter: str | None = None
    contract_candidates: list[str] = field(default_factory=list)
    ranking_terms: dict = field(default_factory=dict)  # debug: ranking-query term -> weight
    verification: dict | None = None  # evidence-support verdict (only when the verifier is enabled)

    def signal_text(self) -> str:
        """Human-readable abstention evidence (shared by CLI and web app)."""
        f = lambda v: "n/a" if v is None else f"{v:.4f}"  # noqa: E731
        from .abstention import DUAL_SIGNALS
        dual = DUAL_SIGNALS.get(self.signal)
        s = f"{dual[1] if dual else self.signal}={f(self.signal_value)} (threshold {self.threshold:.4f})"
        if dual:
            s = f"{dual[0]}={f(self.doc_signal_value)} (threshold {f(self.doc_threshold)}), " + s
        return s

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        if d["verification"] is None:  # absent when the verifier is off => unchanged output
            del d["verification"]
        return d


class Pipeline:
    def __init__(self, cfg: dict, documents: dict[str, str], index: Index | None = None,
                 reranker_scorer: Scorer | None = None, verifier_generator: Generator | None = None):
        self.cfg = cfg
        self.documents = documents
        self.index = index or Index(cfg, documents, reranker_scorer=reranker_scorer)
        vcfg = cfg.get("verifier") or {}
        cache = (resolve_path(cfg["output"]["artifacts_dir"]) / "cache" / "verifier"
                 if vcfg.get("enabled") and vcfg.get("cache", True) else None)
        self.verifier = build_verifier(vcfg, generator=verifier_generator, cache_dir=cache)

    @classmethod
    def from_config(cls, config: str | Path | dict | None = None, overrides: dict | None = None,
                    documents: dict[str, str] | None = None) -> "Pipeline":
        cfg = config if isinstance(config, dict) else load_config(config, overrides)
        if documents is None:
            try:
                tests, _ = load_mini_tests(cfg)
                documents = load_documents(cfg, referenced_documents(tests))
            except FileNotFoundError as e:
                raise PipelineError(str(e)) from e
        return cls(cfg, documents)

    @property
    def max_k(self) -> int:
        return int(self.cfg["retrieval"]["max_k"])

    def resolve_document(self, name: str) -> str:
        """Map an exact document_id or a unique case-insensitive substring to a document_id."""
        if name in self.documents:
            return name
        hits = [d for d in sorted(self.documents) if name.lower() in d.lower()]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            raise PipelineError(f"No indexed contract matches {name!r}.")
        raise PipelineError(f"{name!r} matches {len(hits)} contracts; be more specific: "
                            + "; ".join(h.split('/')[-1] for h in hits[:5]))

    def retrieve(self, query: str, k: int | None = None, document_id: str | None = None) -> RetrievalOutput:
        """Raw ranked retrieval (no abstention). Used by evaluation."""
        if not isinstance(query, str) or not query.strip():
            raise PipelineError("Query is empty.")
        try:
            return self.index.retrieve(query, int(k or self.max_k), document_id=document_id)
        except RerankError as e:  # never fall back silently to the BM25 order
            raise PipelineError(f"Reranking failed: {e}") from e

    def search(self, query: str, top_k: int = 5, document: str | None = None) -> SearchResult:
        """End-to-end search with abstention: what users see in the CLI and web app.

        document: optional exact id or unique substring restricting search to one contract.
        """
        if top_k < 1:
            raise PipelineError("top_k must be >= 1")
        doc_id = self.resolve_document(document) if document else None
        k = max(top_k, self.verifier.top_k) if self.verifier else top_k
        out = self.retrieve(query, k, document_id=doc_id)
        d = decide(len(out.passages), out.signals, self.cfg["abstention"])
        if out.unresolved_contract:
            d.reason = "contract_not_identified"
        verification = None
        # Interactive search skips the model when its verdict cannot change the decision
        # (gate: BM25 already abstains; rescue: BM25 already answers). Evaluation always verifies.
        needed = self.verifier is not None and not (
            (self.verifier.mode == "gate" and d.abstained) or (self.verifier.mode == "rescue" and not d.abstained))
        if needed and out.passages and not out.unresolved_contract:
            v = self.verifier.verify(query, [p.to_dict() for p in out.passages[: self.verifier.top_k]])
            verification = v.to_dict()
            d.abstained, d.reason = apply_verification(d.abstained, d.reason, v, self.verifier.mode, True)
        passages = [] if d.abstained else [p.to_dict() for p in out.passages[:top_k]]
        for p in passages:  # hard guarantee: returned offsets are exact source slices
            if self.documents[p["document_id"]][p["start_offset"]:p["end_offset"]] != p["text"]:
                raise PipelineError(f"Offset invariant violated for {p['document_id']}")
        return SearchResult(query=query, abstained=d.abstained, abstention_reason=d.reason, signal=d.signal,
                            signal_value=d.value, threshold=d.threshold, passages=passages,
                            config_name=self.cfg.get("name", ""), doc_signal_value=d.doc_value,
                            doc_threshold=d.doc_threshold, document_filter=doc_id,
                            contract_candidates=out.contract_candidates, ranking_terms=out.ranking_terms,
                            verification=verification)
