"""Per-query and aggregate evaluation, abstention calibration (train only), artifacts."""

from __future__ import annotations

import csv
import datetime as dt
import json
from pathlib import Path

from .abstention import calibrate, calibrate_dual, decide
from .config import config_fingerprint, dump_config, resolve_path
from .data import Dataset, Query
from .metrics import abstention_metrics, mean_metrics, metrics_at_k
from .pipeline import Pipeline

PREVIEW_CHARS = 160
STORE_TOP = 10


def run_queries(pipeline: Pipeline, queries: list[Query]) -> list[dict]:
    """Inference only: the query text is the only input; gold is attached afterwards."""
    out = []
    for q in queries:
        r = pipeline.retrieve(q.query)
        out.append({
            "qid": q.qid, "query": q.query, "split": q.split, "answerable": q.answerable,
            "category": q.category, "signals": r.signals, "routed_documents": r.routed_documents,
            "passages": [(p.document_id, p.start_offset, p.end_offset, p.score) for p in r.passages],
        })
    return out


def calibrate_threshold(raw_ans: list[dict], raw_neg: list[dict], signal: str) -> dict:
    if signal == "doc_and_chunk":
        pair = lambda r: (r["signals"].get("doc_bm25_norm", 0.0), r["signals"].get("chunk_bm25_norm", 0.0))  # noqa: E731
        res = calibrate_dual([pair(r) for r in raw_ans if r["passages"]],
                             [pair(r) for r in raw_neg if r["passages"]])
        res["signal"] = signal
        res["note"] = "joint (doc, chunk) grid; queries with no candidates always abstain and are excluded"
        return res
    pos = [r["signals"].get(signal, 0.0) for r in raw_ans if r["passages"]]
    neg = [r["signals"].get(signal, 0.0) for r in raw_neg if r["passages"]]
    res = calibrate(pos, neg)
    res["signal"] = signal
    res["note"] = "queries with no candidates always abstain and are excluded from the sweep"
    return res


def score(raw_ans: list[dict], raw_neg: list[dict], queries: dict[str, Query], documents: dict[str, str],
          cfg: dict) -> dict:
    kv = list(cfg["evaluation"]["k_values"])
    rows, raw_rows, e2e_rows, offset_errors = [], [], [], 0
    abst_ans, abst_neg = [], []
    for r in raw_ans + raw_neg:
        for doc, s, e, _ in r["passages"]:
            if not (0 <= s < e <= len(documents.get(doc, ""))):
                offset_errors += 1
        d = decide(len(r["passages"]), r["signals"], cfg["abstention"])
        rec = {"qid": r["qid"], "query": r["query"], "split": r["split"], "answerable": r["answerable"],
               "category": r["category"], "abstained": d.abstained, "abstention_reason": d.reason,
               "signal": d.signal, "signal_value": d.value, "threshold": d.threshold,
               "doc_signal_value": d.doc_value, "doc_threshold": d.doc_threshold,
               "routed_documents": r["routed_documents"],
               "retrieved": [{"rank": i + 1, "document_id": doc, "start_offset": s, "end_offset": e,
                              "score": sc, "preview": documents[doc][s:e][:PREVIEW_CHARS]}
                             for i, (doc, s, e, sc) in enumerate(r["passages"][:STORE_TOP])]}
        if r["answerable"]:
            q = queries[r["qid"]]
            gold = [(g.document_id, g.start, g.end) for g in q.gold]
            spans = [(doc, s, e) for doc, s, e, _ in r["passages"]]
            m_raw = metrics_at_k(spans, gold, kv)
            m_e2e = metrics_at_k([] if d.abstained else spans, gold, kv)
            rec["gold"] = [{"document_id": g.document_id, "start_offset": g.start, "end_offset": g.end,
                            "preview": g.answer[:PREVIEW_CHARS]} for g in q.gold]
            rec["metrics"] = m_raw
            rec["metrics_with_abstention"] = m_e2e
            raw_rows.append(m_raw)
            e2e_rows.append(m_e2e)
            abst_ans.append(d.abstained)
        else:
            abst_neg.append(d.abstained)
        rows.append(rec)
    return {
        "retrieval": mean_metrics(raw_rows),  # official benchmark metrics, no abstention
        "retrieval_with_abstention": mean_metrics(e2e_rows),  # abstained => empty list
        "abstention": abstention_metrics(abst_ans, abst_neg),
        "offset_errors": offset_errors,
        "per_query": rows,
    }


def evaluate(cfg: dict, dataset: Dataset, split: str, *, calibrate_on_train: bool | None = None,
             allow_test: bool = False, pipeline: Pipeline | None = None) -> dict:
    if split == "test" and not allow_test:
        raise PermissionError("Refusing to evaluate the held-out TEST split without --final-test.")
    if split not in {"train", "test"}:
        raise ValueError("split must be train|test")
    pipeline = pipeline or Pipeline(cfg, dataset.documents)
    ans, neg = dataset.split(split, True), dataset.split(split, False)
    raw_ans, raw_neg = run_queries(pipeline, ans), run_queries(pipeline, neg)
    do_cal = cfg["abstention"]["calibrate"] if calibrate_on_train is None else calibrate_on_train
    calibration = None
    if split == "train" and do_cal:
        calibration = calibrate_threshold(raw_ans, raw_neg, cfg["abstention"]["signal"])
        cfg = json.loads(json.dumps(cfg))
        cfg["abstention"]["threshold"] = calibration["threshold"]
        if "doc_threshold" in calibration:
            cfg["abstention"]["doc_threshold"] = calibration["doc_threshold"]
        pipeline.cfg = cfg
    res = score(raw_ans, raw_neg, {q.qid: q for q in ans}, dataset.documents, cfg)
    res.update({
        "split": split, "config_name": cfg.get("name"), "config_fingerprint": config_fingerprint(cfg),
        "config": cfg, "calibration": calibration,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    })
    return res


def write_results(res: dict, out_dir: str | Path) -> Path:
    out = resolve_path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "per_query.jsonl", "w", encoding="utf-8") as f:
        for row in res["per_query"]:
            f.write(json.dumps(row) + "\n")
    summary = {k: v for k, v in res.items() if k not in {"per_query", "config"}}
    (out / "metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    dump_config(res["config"], out / "config_used.yaml")
    kv = res["config"]["evaluation"]["k_values"]
    with open(out / "metrics_by_k.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["mode", "k", "precision", "recall", "f1", "n_queries"])
        for mode in ("retrieval", "retrieval_with_abstention"):
            m = res[mode]
            for k in kv:
                if m.get("n"):
                    w.writerow([mode, k, f"{m[f'precision@{k}']:.4f}", f"{m[f'recall@{k}']:.4f}",
                                f"{m[f'f1@{k}']:.4f}", m["n"]])
    return out


def record_test_run(cfg: dict, out_dir: Path, artifacts_dir: str) -> int:
    log = resolve_path(artifacts_dir) / "test_runs.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    n = sum(1 for _ in open(log, encoding="utf-8")) if log.exists() else 0
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps({"run": n + 1, "config_name": cfg.get("name"),
                            "config_fingerprint": config_fingerprint(cfg), "output": str(out_dir),
                            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}) + "\n")
    return n + 1


def format_summary(res: dict) -> str:
    kv = res["config"]["evaluation"]["k_values"]
    r, e, a = res["retrieval"], res["retrieval_with_abstention"], res["abstention"]
    lines = [f"split={res['split']}  config={res['config_name']}  answerable n={r.get('n', 0)}  "
             f"unanswerable n={a['n_unanswerable']}  offset_errors={res['offset_errors']}",
             f"{'k':>4} {'P':>7} {'R':>7} {'F1':>7} | {'P(abst)':>8} {'R(abst)':>8}"]
    for k in kv:
        if r.get("n"):
            lines.append(f"{k:>4} {r[f'precision@{k}']:7.4f} {r[f'recall@{k}']:7.4f} {r[f'f1@{k}']:7.4f} | "
                         f"{e[f'precision@{k}']:8.4f} {e[f'recall@{k}']:8.4f}")
    cal = res.get("calibration")
    ab = res["config"]["abstention"]
    extra = f" doc_threshold={ab['doc_threshold']:.4f}" if ab["signal"] == "doc_and_chunk" else ""
    lines.append(f"abstention signal={ab['signal']} threshold={ab['threshold']:.4f}{extra}"
                 + (" (calibrated on train)" if cal else " (from config)"))
    fmt = lambda v: "n/a" if v is None else f"{v:.3f}"  # noqa: E731
    lines.append(f"false_abstention_rate={fmt(a['false_abstention_rate'])} ({a['false_abstentions']}/{a['n_answerable']})  "
                 f"correct_abstention_rate={fmt(a['correct_abstention_rate'])} ({a['correct_abstentions']}/{a['n_unanswerable']})  "
                 f"failure_to_abstain_rate={fmt(a['failure_to_abstain_rate'])}  balanced_acc={fmt(a['balanced_accuracy'])}")
    return "\n".join(lines)
