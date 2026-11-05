"""Per-query and aggregate evaluation, abstention calibration (train only), artifacts."""

from __future__ import annotations

import csv
import datetime as dt
import json
import resource
import time
from pathlib import Path

from .abstention import DUAL_SIGNALS, calibrate, calibrate_dual, decide
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
        t0 = time.perf_counter()
        r = pipeline.retrieve(q.query)
        seconds = time.perf_counter() - t0
        rec = {
            "qid": q.qid, "query": q.query, "split": q.split, "answerable": q.answerable,
            "category": q.category, "signals": r.signals, "routed_documents": r.routed_documents,
            "unresolved_contract": r.unresolved_contract,
            "expansion_terms": {t: w for t, w in r.ranking_terms.items() if w < 1.0},
            "passages": [(p.document_id, p.start_offset, p.end_offset, p.score) for p in r.passages],
            "query_seconds": seconds,
        }
        if r.timings:  # reranking ran: keep per-passage second-stage evidence next to the BM25 score
            rec["timings"] = r.timings
            rec["rerank"] = [(p.rerank_score, p.bm25_rank) for p in r.passages]
        out.append(rec)
    return out


def operational_metrics(raw: list[dict], pipeline: Pipeline, index_seconds: float | None) -> dict:
    """Wall-clock and memory measurements for one evaluation process (not quality metrics)."""
    n = len(raw)
    qs = [r.get("query_seconds", 0.0) for r in raw]
    rr = [r["timings"]["rerank_seconds"] for r in raw if r.get("timings")]
    scorer = getattr(getattr(pipeline.index, "reranker", None), "scorer", None)
    # Linux reports ru_maxrss in KiB: peak resident memory of the whole process so far.
    peak_mib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    return {
        "n_queries": n,
        "index_build_seconds": index_seconds,
        "mean_query_seconds": sum(qs) / n if n else None,
        "total_query_seconds": sum(qs),
        "n_reranked_queries": len(rr),
        "mean_rerank_seconds": sum(rr) / len(rr) if rr else None,
        "mean_candidates_reranked": (sum(r["timings"]["n_reranked"] for r in raw if r.get("timings")) / len(rr)
                                     if rr else None),
        "reranker_model_load_seconds": getattr(scorer, "load_seconds", None),
        "reranker_n_parameters": getattr(scorer, "n_parameters", None),
        "peak_rss_mib": round(peak_mib, 1),
        "note": "first reranked query includes lazy model loading in its query_seconds; "
                "mean_rerank_seconds excludes loading",
    }


def calibrate_threshold(raw_ans: list[dict], raw_neg: list[dict], signal: str) -> dict:
    if signal in DUAL_SIGNALS:
        id_key, ans_key = DUAL_SIGNALS[signal]
        pair = lambda r: (r["signals"].get(id_key, 0.0), r["signals"].get(ans_key, 0.0))  # noqa: E731
        res = calibrate_dual([pair(r) for r in raw_ans if r["passages"]],
                             [pair(r) for r in raw_neg if r["passages"]])
        res["signal"] = signal
        res["note"] = (f"joint ({id_key}, {ans_key}) grid; queries with no candidates always abstain "
                       "and are excluded")
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
        if r.get("unresolved_contract"):
            d.reason = "contract_not_identified"
        rec = {"qid": r["qid"], "query": r["query"], "split": r["split"], "answerable": r["answerable"],
               "category": r["category"], "abstained": d.abstained, "abstention_reason": d.reason,
               "signal": d.signal, "signal_value": d.value, "threshold": d.threshold,
               "doc_signal_value": d.doc_value, "doc_threshold": d.doc_threshold,
               "routed_documents": r["routed_documents"], "expansion_terms": r.get("expansion_terms", {}),
               "retrieved": [{"rank": i + 1, "document_id": doc, "start_offset": s, "end_offset": e,
                              "score": sc, "preview": documents[doc][s:e][:PREVIEW_CHARS]}
                             for i, (doc, s, e, sc) in enumerate(r["passages"][:STORE_TOP])]}
        if r.get("rerank"):
            for item, (rs, br) in zip(rec["retrieved"], r["rerank"]):
                item["rerank_score"], item["bm25_rank"] = rs, br
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
    index_seconds = None
    if pipeline is None:
        t0 = time.perf_counter()
        pipeline = Pipeline(cfg, dataset.documents)
        index_seconds = time.perf_counter() - t0
    ans, neg = dataset.split(split, True), dataset.split(split, False)
    raw_ans, raw_neg = run_queries(pipeline, ans), run_queries(pipeline, neg)
    operational = operational_metrics(raw_ans + raw_neg, pipeline, index_seconds)
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
        "config": cfg, "calibration": calibration, "operational": operational,
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
    op = res.get("operational")
    if op:
        lines.append(f"operational: index_build_s={fmt(op['index_build_seconds'])}  "
                     f"mean_query_s={fmt(op['mean_query_seconds'])}  mean_rerank_s={fmt(op['mean_rerank_seconds'])}  "
                     f"model_load_s={fmt(op['reranker_model_load_seconds'])}  peak_rss_mib={op['peak_rss_mib']}")
    return "\n".join(lines)
