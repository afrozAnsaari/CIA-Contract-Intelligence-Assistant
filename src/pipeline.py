"""The single query pipeline shared by the CLI, the Streamlit app and evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .abstention import decide
from .config import load_config
from .data import load_documents, load_mini_tests, referenced_documents
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

    def to_dict(self) -> dict:
        return dict(self.__dict__)


class Pipeline:
    def __init__(self, cfg: dict, documents: dict[str, str], index: Index | None = None):
        self.cfg = cfg
        self.documents = documents
        self.index = index or Index(cfg, documents)

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

    def retrieve(self, query: str, k: int | None = None) -> RetrievalOutput:
        """Raw ranked retrieval (no abstention). Used by evaluation."""
        if not isinstance(query, str) or not query.strip():
            raise PipelineError("Query is empty.")
        return self.index.retrieve(query, int(k or self.max_k))

    def search(self, query: str, top_k: int = 5) -> SearchResult:
        """End-to-end search with abstention: what users see in the CLI and web app."""
        if top_k < 1:
            raise PipelineError("top_k must be >= 1")
        out = self.retrieve(query, top_k)
        d = decide(len(out.passages), out.signals, self.cfg["abstention"])
        passages = [] if d.abstained else [p.to_dict() for p in out.passages[:top_k]]
        for p in passages:  # hard guarantee: returned offsets are exact source slices
            if self.documents[p["document_id"]][p["start_offset"]:p["end_offset"]] != p["text"]:
                raise PipelineError(f"Offset invariant violated for {p['document_id']}")
        return SearchResult(query=query, abstained=d.abstained, abstention_reason=d.reason, signal=d.signal,
                            signal_value=d.value, threshold=d.threshold, passages=passages,
                            config_name=self.cfg.get("name", ""))
