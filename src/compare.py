"""Side-by-side comparison of saved evaluation runs (read-only; never re-runs anything).

Inputs per run directory: metrics.json and per_query.jsonl written by `evaluate`.
  - P/R/F1 at k in evaluation.k_values come from metrics.json unchanged.
  - Metrics at other k <= 10 (e.g. recall@10) are recomputed with src/metrics.py from the stored
    top-10 passages (`retrieved`, STORE_TOP = 10) and gold spans; k = 5 is recomputed as well and
    checked against metrics.json so the recomputation is verified.
  - Per-query case table: rank of the first top-10 passage overlapping gold (">10" otherwise),
    the abstention decision and, for reranked runs, that passage's BM25 rank and reranker score.
"""

from __future__ import annotations

import json
from pathlib import Path

from .config import resolve_path
from .metrics import mean_metrics, metrics_at_k

STORED_TOP = 10


def load_run(path: str | Path) -> dict:
    d = resolve_path(path)
    m = json.loads((d / "metrics.json").read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in open(d / "per_query.jsonl", encoding="utf-8")]
    return {"dir": str(d), "name": d.name, "metrics": m, "rows": rows}


def _spans(items: list[dict]) -> list[tuple[str, int, int]]:
    return [(x["document_id"], x["start_offset"], x["end_offset"]) for x in items]


def recomputed(run: dict, ks: list[int]) -> dict:
    ans = [r for r in run["rows"] if r["answerable"]]
    rows = [metrics_at_k(_spans(r["retrieved"]), _spans(r["gold"]), ks) for r in ans]
    return mean_metrics(rows)


def first_gold_rank(row: dict) -> int | None:
    gold = _spans(row.get("gold", []))
    for item in row["retrieved"]:
        if any(item["document_id"] == g[0] and item["start_offset"] < g[2] and g[1] < item["end_offset"]
               for g in gold):
            return item["rank"]
    return None


def _with_answerability(a: dict) -> dict:
    """Derive answer precision/recall from stored counts for runs written before those keys existed."""
    a = dict(a)
    if "answer_precision" not in a and a.get("n_answerable") is not None:
        tp, fp = a["n_answerable"] - a["false_abstentions"], a["n_unanswerable"] - a["correct_abstentions"]
        a["answer_precision"] = tp / (tp + fp) if tp + fp else None
        a["answer_recall"] = tp / a["n_answerable"] if a["n_answerable"] else None
    return a


def compare(run_dirs: list[str], ks: list[int], extra_ks: list[int], qids: list[str]) -> dict:
    runs = [load_run(d) for d in run_dirs]
    for k in extra_ks:
        if k > STORED_TOP:
            raise ValueError(f"k={k} exceeds the {STORED_TOP} passages stored per query")
    out = {"runs": [], "cases": [], "vs_first": []}
    for run in runs:
        m = run["metrics"]
        rec = recomputed(run, sorted(set(extra_ks) | {5}))
        check = abs(rec["recall@5"] - m["retrieval"]["recall@5"]) < 1e-9 and \
            abs(rec["precision@5"] - m["retrieval"]["precision@5"]) < 1e-9
        out["runs"].append({
            "name": run["name"], "config": m.get("config_name"), "split": m.get("split"),
            "retrieval": {f"{x}@{k}": m["retrieval"][f"{x}@{k}"] for k in ks for x in ("precision", "recall", "f1")
                          if f"{x}@{k}" in m["retrieval"]},
            "recomputed": {f"{x}@{k}": rec[f"{x}@{k}"] for k in extra_ks for x in ("precision", "recall", "f1")},
            "recompute_matches_metrics_json": check,
            "abstention": _with_answerability(m["abstention"]),
            "threshold": (m.get("calibration") or {}).get("threshold"),
            "offset_errors": m.get("offset_errors"), "operational": m.get("operational"),
            "n_answerable": m["retrieval"].get("n"),
        })
    by_qid = [{r["qid"]: r for r in run["rows"]} for run in runs]
    for q in qids:
        case = {"qid": q, "query": by_qid[0].get(q, {}).get("query"), "per_run": []}
        for run, rows in zip(runs, by_qid):
            r = rows.get(q)
            if r is None:
                case["per_run"].append({"run": run["name"], "missing": True})
                continue
            rank = first_gold_rank(r)
            item = r["retrieved"][rank - 1] if rank else None
            case["per_run"].append({"run": run["name"], "first_gold_rank": rank, "abstained": r["abstained"],
                                    "verifier": (r.get("verification") or {}).get("decision"),
                                    "signal_value": r["signal_value"],
                                    "bm25_rank": item.get("bm25_rank") if item else None,
                                    "rerank_score": item.get("rerank_score") if item else None,
                                    "top1_rerank_score": (r["retrieved"][0].get("rerank_score")
                                                          if r["retrieved"] else None)})
        out["cases"].append(case)
    base = by_qid[0]
    for run, rows in zip(runs[1:], by_qid[1:]):
        common = [q for q in base if q in rows]
        top1 = sum(1 for q in common if base[q]["retrieved"][:1] and rows[q]["retrieved"][:1]
                   and _spans(base[q]["retrieved"][:1]) != _spans(rows[q]["retrieved"][:1]))
        abst = [q for q in common if base[q]["abstained"] != rows[q]["abstained"]]
        out["vs_first"].append({"run": run["name"], "vs": runs[0]["name"], "n_common": len(common),
                                "top1_passage_changed": top1, "abstention_decision_changed": abst})
    return out


def format_comparison(c: dict) -> str:
    f = lambda v, n=4: "n/a" if v is None else (f"{v:.{n}f}" if isinstance(v, float) else str(v))  # noqa: E731
    names = [r["name"] for r in c["runs"]]
    lines = ["| metric | " + " | ".join(names) + " |", "|---|" + "---:|" * len(names)]
    keys = list(c["runs"][0]["retrieval"]) + list(c["runs"][0]["recomputed"])
    for key in keys:
        src = "retrieval" if key in c["runs"][0]["retrieval"] else "recomputed"
        label = key + (" (top-10 recompute)" if src == "recomputed" else "")
        lines.append(f"| {label} | " + " | ".join(f(r[src].get(key)) for r in c["runs"]) + " |")
    for key in ("false_abstentions", "correct_abstentions", "failures_to_abstain", "false_abstention_rate",
                "correct_abstention_rate", "failure_to_abstain_rate", "balanced_accuracy",
                "answer_precision", "answer_recall"):
        lines.append(f"| {key} | " + " | ".join(f(r["abstention"].get(key), 3) for r in c["runs"]) + " |")
    lines.append("| calibrated threshold | " + " | ".join(f(r["threshold"]) for r in c["runs"]) + " |")
    lines.append("| offset errors | " + " | ".join(f(r["offset_errors"]) for r in c["runs"]) + " |")
    lines.append("| recompute check (k=5) | " + " | ".join("ok" if r["recompute_matches_metrics_json"]
                                                          else "MISMATCH" for r in c["runs"]) + " |")
    op_keys = ("index_build_seconds", "mean_query_seconds", "mean_rerank_seconds", "mean_candidates_reranked",
               "reranker_model_load_seconds", "reranker_n_parameters", "peak_rss_mib",
               "n_verified_queries", "n_verifier_generated", "mean_verification_seconds",
               "verifier_model_load_seconds", "verifier_model_bytes")
    if any(r["operational"] for r in c["runs"]):
        for key in op_keys:
            lines.append(f"| {key} | " + " | ".join(f((r["operational"] or {}).get(key), 4) for r in c["runs"]) + " |")
    for d in c["vs_first"]:
        lines.append(f"\n{d['run']} vs {d['vs']}: top-1 passage changed on {d['top1_passage_changed']}/"
                     f"{d['n_common']} queries; abstention decision changed on "
                     f"{len(d['abstention_decision_changed'])} ({', '.join(d['abstention_decision_changed']) or 'none'})")
    if c["cases"]:
        lines.append("\n| case | " + " | ".join(names) + " |")
        lines.append("|---|" + "---|" * len(names))
        for case in c["cases"]:
            cells = []
            for p in case["per_run"]:
                if p.get("missing"):
                    cells.append("missing")
                    continue
                s = str(p["first_gold_rank"]) if p["first_gold_rank"] else ">10"
                if p["abstained"]:
                    s += " (abst.)"
                if p.get("verifier"):
                    s += f" {{v: {p['verifier']}}}"
                if p["bm25_rank"] is not None:
                    s += f" [bm25 {p['bm25_rank']}, ce {p['rerank_score']:.2f}]"
                cells.append(s)
            lines.append(f"| {case['qid']} | " + " | ".join(cells) + " |")
    return "\n".join(lines)
