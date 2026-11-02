"""Post-hoc failure categorisation (uses gold labels; never feeds back into inference).

Answerable queries, judged on the top-k list (k = evaluation.primary_k), in priority order:
  offset_error       a returned passage is not a valid slice of its source document
  false_abstention   pipeline abstained on an answerable query
  wrong_document     no top-k passage comes from any gold document
  wrong_section      right document(s) but zero character overlap with gold
  chunk_boundary     some gold span is only partially covered and is cut by a returned
                     passage boundary while being short enough (<= max_chars) to fit
  partial_span       some gold text found but recall@k < 1 (e.g. multi-span answers)
  low_rank           recall@k == 1 but the top-1 passage has no gold overlap
  irrelevant_extra   recall@k == 1 but precision@k < low_precision_threshold
  ok                 none of the above
Unanswerable queries: correct_abstention | failure_to_abstain.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from .config import resolve_path

FAILURES = ["offset_error", "false_abstention", "wrong_document", "wrong_section", "chunk_boundary",
            "partial_span", "low_rank", "irrelevant_extra", "failure_to_abstain"]


def _overlap(a0: int, a1: int, b0: int, b1: int) -> int:
    return max(0, min(a1, b1) - max(a0, b0))


def categorize(row: dict, k: int, max_chars: int, documents: dict[str, str] | None = None,
               low_precision_threshold: float = 0.1) -> str:
    if not row["answerable"]:
        return "correct_abstention" if row["abstained"] else "failure_to_abstain"
    top = row["retrieved"][:k]
    if documents is not None:
        for p in top:
            if not (0 <= p["start_offset"] < p["end_offset"] <= len(documents.get(p["document_id"], ""))):
                return "offset_error"
    if row["abstained"]:
        return "false_abstention"
    m = row["metrics"]
    gold = row["gold"]
    gold_docs = {g["document_id"] for g in gold}
    if not any(p["document_id"] in gold_docs for p in top):
        return "wrong_document"
    if m[f"recall@{k}"] <= 0:
        return "wrong_section"
    if m[f"recall@{k}"] < 1 - 1e-9:
        for g in gold:
            glen = g["end_offset"] - g["start_offset"]
            for p in top:
                if p["document_id"] != g["document_id"]:
                    continue
                ov = _overlap(p["start_offset"], p["end_offset"], g["start_offset"], g["end_offset"])
                if 0 < ov < glen and glen <= max_chars:
                    return "chunk_boundary"
        return "partial_span"
    t1 = top[0]
    if not any(t1["document_id"] == g["document_id"] and
               _overlap(t1["start_offset"], t1["end_offset"], g["start_offset"], g["end_offset"]) > 0 for g in gold):
        return "low_rank"
    if m[f"precision@{k}"] < low_precision_threshold:
        return "irrelevant_extra"
    return "ok"


def diagnose(per_query: list[dict], cfg: dict, documents: dict[str, str] | None = None) -> dict:
    k = int(cfg["evaluation"]["primary_k"])
    max_chars = int(cfg["chunking"]["max_chars"])
    counts: Counter = Counter()
    records = []
    for row in per_query:
        cat = categorize(row, k, max_chars, documents)
        counts[cat] += 1
        records.append({**row, "category_diagnosis": cat})
    n_ans = sum(r["answerable"] for r in per_query)
    ans_fail = {c: n for c, n in counts.items() if c in FAILURES and c != "failure_to_abstain"}
    dominant = max(sorted(ans_fail), key=lambda c: ans_fail[c]) if ans_fail else None
    return {"k": k, "counts": dict(sorted(counts.items())), "n_answerable": n_ans,
            "n_unanswerable": len(per_query) - n_ans, "dominant_answerable_failure": dominant,
            "records": records}


def error_analysis(per_query: list[dict], cfg: dict, documents: dict[str, str], out_dir: str | Path,
                   config_label: str, per_category: int = 4) -> dict:
    """Write machine-readable failures + a grouped markdown digest (train data only)."""
    diag = diagnose(per_query, cfg, documents)
    out = resolve_path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    k = diag["k"]
    groups: dict[str, list[dict]] = defaultdict(list)
    with open(out / "failures.jsonl", "w", encoding="utf-8") as f:
        for r in diag["records"]:
            cat = r["category_diagnosis"]
            if cat in ("ok", "correct_abstention"):
                continue
            item = {"config": config_label, "category": cat, "qid": r["qid"], "query": r["query"],
                    "split": r["split"], "signal_value": r["signal_value"], "threshold": r["threshold"],
                    "gold": r.get("gold", []), "retrieved_top_k": r["retrieved"][:k],
                    "metrics_at_k": {m: r["metrics"][f"{m}@{k}"] for m in ("precision", "recall")}
                    if r.get("metrics") else None}
            f.write(json.dumps(item) + "\n")
            groups[cat].append(item)
    summary = {"config": config_label, "k": k, "counts": diag["counts"],
               "dominant_answerable_failure": diag["dominant_answerable_failure"],
               "n_failures": sum(len(v) for v in groups.values())}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [f"# Error analysis ({config_label}, split={per_query[0]['split'] if per_query else '?'}, k={k})", "",
             "Counts: " + ", ".join(f"{c}={n}" for c, n in diag["counts"].items()), ""]
    for cat in FAILURES:
        items = groups.get(cat, [])
        if not items:
            continue
        lines.append(f"## {cat} ({len(items)})")
        for it in items[:per_category]:
            lines.append(f"- **{it['qid']}**: {it['query']}")
            for g in it["gold"]:
                lines.append(f"  - gold: `{g['document_id']}` [{g['start_offset']}:{g['end_offset']}] "
                             f"\"{g['preview'][:100]}...\"")
            for p in it["retrieved_top_k"][:3]:
                lines.append(f"  - got #{p['rank']}: `{p['document_id']}` [{p['start_offset']}:{p['end_offset']}] "
                             f"score={p['score']:.3f} \"{p['preview'][:100]}...\"")
            if it["metrics_at_k"]:
                lines.append(f"  - P@{k}={it['metrics_at_k']['precision']:.3f} R@{k}={it['metrics_at_k']['recall']:.3f}"
                             f" signal={it['signal_value']}")
        lines.append("")
    (out / "error_analysis.md").write_text("\n".join(lines), encoding="utf-8")
    return summary
