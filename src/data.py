"""Benchmark loading, exact LegalBench-RAG-mini selection, deterministic split, validation.

Source text is always read with Python's default text-mode UTF-8 decoding
(`open(path, encoding="utf-8").read()`), which is the convention the benchmark's
character offsets are defined against. Source text is never normalised or altered.
"""

from __future__ import annotations

import hashlib
import json
import random
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from .config import resolve_path

# ----------------------------------------------------------------------------
# Prescribed protocol (copied verbatim in behaviour from the assignment)
# ----------------------------------------------------------------------------


def mini(tests, n=194):
    if len(tests) <= n:
        return tests

    def key(t):
        random.seed(t["snippets"][0]["file_path"])
        return random.random()

    return sorted(tests, key=key)[:n]


def assign_split(query: str) -> str:
    h = int(hashlib.sha256(query.strip().encode("utf-8")).hexdigest(), 16)
    return "test" if h % 10 < 3 else "train"


# ----------------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------------


@dataclass(frozen=True)
class GoldSpan:
    document_id: str
    start: int
    end: int
    answer: str


@dataclass(frozen=True)
class Query:
    qid: str
    query: str
    split: str
    gold: tuple[GoldSpan, ...] = ()
    answerable: bool = True
    category: str = ""
    rationale: str = ""
    absence_terms: tuple[str, ...] = ()


@dataclass
class Dataset:
    queries: list[Query]  # answerable benchmark queries (both splits)
    negatives: list[Query]  # unanswerable queries (both splits)
    documents: dict[str, str]  # document_id -> original source text
    meta: dict = field(default_factory=dict)

    def split(self, name: str, answerable: bool = True) -> list[Query]:
        if name not in {"train", "test"}:
            raise ValueError(f"split must be train|test, got {name!r}")
        pool = self.queries if answerable else self.negatives
        return [q for q in pool if q.split == name]


def read_source(path: Path) -> str:
    """Python default text-mode read (universal newlines) of a UTF-8 file."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def make_qid(query: str, first_file: str) -> str:
    return "cuad-" + hashlib.sha256(f"{query}|{first_file}".encode("utf-8")).hexdigest()[:10]


def tests_to_queries(tests: list[dict]) -> list[Query]:
    out, seen = [], set()
    for t in tests:
        qid = make_qid(t["query"], t["snippets"][0]["file_path"])
        if qid in seen:  # pragma: no cover - defensive, benchmark has no exact duplicates
            raise ValueError(f"Duplicate query id {qid}")
        seen.add(qid)
        gold = tuple(
            GoldSpan(s["file_path"], int(s["span"][0]), int(s["span"][1]), s["answer"]) for s in t["snippets"]
        )
        out.append(Query(qid=qid, query=t["query"], split=assign_split(t["query"]), gold=gold))
    return out


def referenced_documents(tests: list[dict]) -> list[str]:
    return sorted({s["file_path"] for t in tests for s in t["snippets"]})


# ----------------------------------------------------------------------------
# Preparation (copy only the needed assets into data/raw, idempotently)
# ----------------------------------------------------------------------------


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _load_sha256sums(source: Path) -> dict[str, str]:
    p = source / "SHA256SUMS"
    sums: dict[str, str] = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                sums[parts[1].lstrip("*").lstrip("./")] = parts[0]
    return sums


def prepare_data(source: str | Path, cfg: dict) -> dict:
    """Copy benchmarks/cuad.json + only the CUAD contracts referenced by the mini set."""
    source = Path(source).expanduser().resolve()
    bench_rel = cfg["data"]["benchmark"]
    src_bench = source / bench_rel
    if not src_bench.exists():
        raise FileNotFoundError(f"{src_bench} not found. Is --source the LegalBench-RAG root?")
    dest = resolve_path(cfg["data"]["raw_dir"])
    tests_all = json.loads(read_source(src_bench))["tests"]
    selected = mini(tests_all, cfg["data"]["mini_n"])
    docs = referenced_documents(selected)
    sums = _load_sha256sums(source)

    copied, skipped, checksum_ok, checksum_missing = 0, 0, 0, 0
    files = [bench_rel] + [f"corpus/{d}" for d in docs]
    for rel in files:
        src, dst = source / rel, dest / rel
        if not src.exists():
            raise FileNotFoundError(f"Referenced file missing in source: {src}")
        src_hash = _sha256_file(src)
        if rel in sums:
            if sums[rel] != src_hash:
                raise ValueError(f"SHA256 mismatch for {rel} in source dataset")
            checksum_ok += 1
        else:
            checksum_missing += 1
        if dst.exists() and _sha256_file(dst) == src_hash:
            skipped += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)  # byte-identical copy
        copied += 1

    queries = tests_to_queries(selected)
    processed = resolve_path(cfg["data"]["processed_dir"])
    processed.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": str(source),
        "benchmark_total_tests": len(tests_all),
        "mini_n": len(selected),
        "documents": docs,
        "n_documents": len(docs),
        "split_counts": {s: sum(q.split == s for q in queries) for s in ("train", "test")},
        "files_copied": copied,
        "files_unchanged": skipped,
        "checksums_verified": checksum_ok,
        "checksums_unavailable": checksum_missing,
    }
    (processed / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    with open(processed / "cuad_mini_queries.jsonl", "w", encoding="utf-8") as f:
        for q in queries:
            f.write(json.dumps({"qid": q.qid, "split": q.split, "query": q.query,
                                "gold": [g.__dict__ for g in q.gold]}) + "\n")
    return manifest


# ----------------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------------


def load_mini_tests(cfg: dict) -> tuple[list[dict], int]:
    raw = resolve_path(cfg["data"]["raw_dir"])
    bench = raw / cfg["data"]["benchmark"]
    if not bench.exists():
        raise FileNotFoundError(
            f"Benchmark not found at {bench}. Run: python -m src.cli prepare-data --source <legalbench-rag root>"
        )
    tests = json.loads(read_source(bench))["tests"]
    n = cfg["data"]["mini_n"]
    selected = mini(tests, n)
    if len(tests) >= n and len(selected) != n:
        raise ValueError(f"mini() selected {len(selected)} queries, expected {n}")
    return selected, len(tests)


def load_documents(cfg: dict, doc_ids: list[str]) -> dict[str, str]:
    corpus = resolve_path(cfg["data"]["raw_dir"]) / "corpus"
    docs = {}
    for d in doc_ids:
        p = corpus / d
        if not p.exists():
            raise FileNotFoundError(f"Document missing: {p}. Re-run prepare-data.")
        docs[d] = read_source(p)
    return docs


def load_unanswerable(cfg: dict) -> list[Query]:
    p = resolve_path(cfg["data"]["unanswerable_path"])
    if not p.exists():
        raise FileNotFoundError(f"Unanswerable query set not found: {p}")
    payload = json.loads(read_source(p))
    out = []
    for item in payload["queries"]:
        out.append(Query(qid=item["id"], query=item["query"], split=assign_split(item["query"]),
                         gold=(), answerable=False, category=item.get("category", ""),
                         rationale=item.get("rationale", ""),
                         absence_terms=tuple(item.get("absence_check_terms", []))))
    return out


def load_dataset(cfg: dict, with_negatives: bool = True) -> Dataset:
    selected, total = load_mini_tests(cfg)
    queries = tests_to_queries(selected)
    doc_ids = referenced_documents(selected)
    documents = load_documents(cfg, doc_ids)
    negatives = load_unanswerable(cfg) if with_negatives else []
    return Dataset(queries=queries, negatives=negatives, documents=documents,
                   meta={"benchmark_total_tests": total, "n_documents": len(doc_ids)})


# ----------------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------------


def validate_dataset(ds: Dataset) -> dict:
    """Checks gold slices, split partition, and negative-set integrity. Returns a report."""
    gold_total, gold_bad, bad_examples = 0, 0, []
    for q in ds.queries:
        for g in q.gold:
            gold_total += 1
            text = ds.documents.get(g.document_id)
            if text is None or text[g.start:g.end] != g.answer:
                gold_bad += 1
                if len(bad_examples) < 5:
                    bad_examples.append({"qid": q.qid, "document_id": g.document_id, "span": [g.start, g.end]})
    referenced = {g.document_id for q in ds.queries for g in q.gold}
    neg_ids = [n.qid for n in ds.negatives]
    neg_texts = [n.query.strip().lower() for n in ds.negatives]
    bench_texts = {q.query.strip().lower() for q in ds.queries}
    lowered = {d: t.lower() for d, t in ds.documents.items()}
    absence_hits = {n.qid: [t for t in n.absence_terms if any(t.lower() in x for x in lowered.values())]
                    for n in ds.negatives}
    absence_hits = {k: v for k, v in absence_hits.items() if v}
    report = {
        "n_queries": len(ds.queries),
        "split_counts": {s: sum(q.split == s for q in ds.queries) for s in ("train", "test")},
        "n_documents_indexed": len(ds.documents),
        "indexed_equals_referenced": set(ds.documents) == referenced,
        "gold_spans_total": gold_total,
        "gold_spans_mismatched": gold_bad,
        "gold_mismatch_examples": bad_examples,
        "split_partition_ok": all(q.split == assign_split(q.query) for q in ds.queries + ds.negatives),
        "n_unanswerable": len(ds.negatives),
        "unanswerable_split_counts": {s: sum(n.split == s for n in ds.negatives) for s in ("train", "test")},
        "unanswerable_ids_unique": len(set(neg_ids)) == len(neg_ids),
        "unanswerable_queries_unique": len(set(neg_texts)) == len(neg_texts),
        "unanswerable_overlap_with_benchmark": sorted(set(neg_texts) & bench_texts),
        "unanswerable_all_have_rationale": all(n.rationale.strip() for n in ds.negatives),
        "unanswerable_absence_term_hits": absence_hits,
    }
    report["ok"] = bool(
        report["gold_spans_mismatched"] == 0
        and report["indexed_equals_referenced"]
        and report["split_partition_ok"]
        and report["n_unanswerable"] >= 30
        and report["unanswerable_ids_unique"]
        and report["unanswerable_queries_unique"]
        and not report["unanswerable_overlap_with_benchmark"]
        and report["unanswerable_all_have_rationale"]
        and not absence_hits
    )
    return report


def unanswerable_set_hash(cfg: dict) -> str:
    return _sha256_file(resolve_path(cfg["data"]["unanswerable_path"]))
