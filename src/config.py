"""Configuration loading: YAML files merged over code defaults, plus dotted overrides.

Every experiment parameter lives here so experiments never need source edits.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULTS: dict[str, Any] = {
    "name": "unnamed",
    "status": "candidate",  # candidate | provisional | final
    "data": {
        "raw_dir": "data/raw/legalbench-rag",  # populated by `prepare-data`
        "benchmark": "benchmarks/cuad.json",
        "mini_n": 194,
        "processed_dir": "data/processed",
        "unanswerable_path": "data/unanswerable_queries.json",
    },
    "chunking": {
        "strategy": "paragraph",  # paragraph (boundary-aware) | fixed (hard cuts)
        "max_chars": 1000,
        "overlap_chars": 150,
        "min_chars": 20,  # drop chunks shorter than this (except a doc's only chunk)
        "boundary_search_frac": 0.3,  # look for a boundary in the last 30% of the window
    },
    "text": {
        "lowercase": True,
        "stopwords": False,
        "stemming": False,
    },
    "query": {
        # CUAD queries look like "Consider the <contract>; <question>".
        # "full": use whole query everywhere. "split": route documents with the
        # contract preamble and rank chunks with `chunk_query` (see below).
        "mode": "full",
        "chunk_query": "full",  # full | question (only used when mode == split)
    },
    "retrieval": {
        "method": "bm25",  # bm25 | dense | hybrid
        "max_k": 64,  # deepest prefix that is ever evaluated
        "overlap_policy": "skip",  # keep | skip | trim  (same-document overlapping passages)
        "min_trimmed_chars": 50,
        "index_doc_title": False,  # prepend file-name tokens to the *indexing* text only
        "bm25": {"k1": 1.5, "b": 0.75},
        "dense": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
            "batch_size": 32,
            "query_prefix": "",
            "passage_prefix": "",
        },
        "hybrid": {"rrf_k": 60, "bm25_weight": 1.0, "dense_weight": 1.0, "pool": 200},
        "doc_routing": {
            "enabled": False,
            "top_n_docs": 1,
            "doc_text": "title_head",  # title_head | full
            "head_chars": 3000,
        },
    },
    "abstention": {
        "enabled": True,
        # Signal options: chunk_bm25_norm | doc_bm25_norm | dense_max_cos
        "signal": "chunk_bm25_norm",
        "threshold": 0.0,  # abstain iff signal < threshold (equality => answer)
        "calibrate": True,  # evaluation/loop recalibrate on TRAIN data only
    },
    "evaluation": {
        "k_values": [1, 2, 4, 5, 8, 16, 32, 64],
        "primary_k": 5,
    },
    "output": {"artifacts_dir": "artifacts"},
}


def deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, val in (override or {}).items():
        if isinstance(val, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], val)
        else:
            out[key] = copy.deepcopy(val)
    return out


def set_dotted(cfg: dict, dotted: str, value: Any) -> dict:
    """Return a copy of cfg with cfg[a][b][c] = value for dotted 'a.b.c'."""
    out = copy.deepcopy(cfg)
    node = out
    parts = dotted.split(".")
    for p in parts[:-1]:
        node = node.setdefault(p, {})
    node[parts[-1]] = copy.deepcopy(value)
    return out


def get_dotted(cfg: dict, dotted: str, default: Any = None) -> Any:
    node: Any = cfg
    for p in dotted.split("."):
        if not isinstance(node, dict) or p not in node:
            return default
        node = node[p]
    return node


def apply_overrides(cfg: dict, overrides: dict[str, Any] | None) -> dict:
    out = cfg
    for k, v in (overrides or {}).items():
        out = set_dotted(out, k, v)
    return out


def load_config(path: str | Path | None = None, overrides: dict[str, Any] | None = None) -> dict:
    cfg = copy.deepcopy(DEFAULTS)
    if path is not None:
        p = resolve_path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config file not found: {p}")
        with p.open(encoding="utf-8") as f:
            user = yaml.safe_load(f) or {}
        cfg = deep_merge(cfg, user)
    cfg = apply_overrides(cfg, overrides)
    validate_config(cfg)
    return cfg


def validate_config(cfg: dict) -> None:
    ch = cfg["chunking"]
    if ch["strategy"] not in {"paragraph", "fixed"}:
        raise ValueError(f"chunking.strategy must be paragraph|fixed, got {ch['strategy']!r}")
    if ch["max_chars"] <= 0:
        raise ValueError("chunking.max_chars must be > 0")
    if not 0 <= ch["overlap_chars"] < ch["max_chars"]:
        raise ValueError("chunking.overlap_chars must be in [0, max_chars)")
    r = cfg["retrieval"]
    if r["method"] not in {"bm25", "dense", "hybrid"}:
        raise ValueError(f"retrieval.method must be bm25|dense|hybrid, got {r['method']!r}")
    if r["overlap_policy"] not in {"keep", "skip", "trim"}:
        raise ValueError("retrieval.overlap_policy must be keep|skip|trim")
    q = cfg["query"]
    if q["mode"] not in {"full", "split"} or q["chunk_query"] not in {"full", "question"}:
        raise ValueError("query.mode must be full|split and query.chunk_query full|question")
    a = cfg["abstention"]
    if a["signal"] not in {"chunk_bm25_norm", "doc_bm25_norm", "dense_max_cos"}:
        raise ValueError(f"Unknown abstention.signal {a['signal']!r}")
    if a["signal"] == "doc_bm25_norm" and not r["doc_routing"]["enabled"]:
        raise ValueError("abstention.signal doc_bm25_norm requires retrieval.doc_routing.enabled")
    if a["signal"] == "dense_max_cos" and r["method"] == "bm25":
        raise ValueError("abstention.signal dense_max_cos requires method dense or hybrid")


def resolve_path(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else REPO_ROOT / p


def index_fingerprint(cfg: dict) -> str:
    """Hash of everything that changes the index (chunks + indexing text + models)."""
    keys = {
        "data": cfg["data"],
        "chunking": cfg["chunking"],
        "text": cfg["text"],
        "index_doc_title": cfg["retrieval"]["index_doc_title"],
        "dense": cfg["retrieval"]["dense"] if cfg["retrieval"]["method"] != "bm25" else None,
    }
    return hashlib.sha256(json.dumps(keys, sort_keys=True).encode()).hexdigest()[:16]


def config_fingerprint(cfg: dict) -> str:
    c = {k: v for k, v in cfg.items() if k not in {"name", "status"}}
    return hashlib.sha256(json.dumps(c, sort_keys=True).encode()).hexdigest()[:16]


def dump_config(cfg: dict, path: str | Path) -> Path:
    p = resolve_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    return p
