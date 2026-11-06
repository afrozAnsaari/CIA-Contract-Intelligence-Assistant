"""Command-line interface. Run from the repository root:

    python -m src.cli search \\
      --query "What restrictions apply to sublicensing?" \\
      --top-k 5

Subcommands: prepare-data, validate-data, build-index, search, show-span, evaluate, improve,
error-analysis, demo-check, compare.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time

DEFAULT_CONFIG = "configs/final.yaml"


def _add_config(p: argparse.ArgumentParser, default: str = DEFAULT_CONFIG) -> None:
    p.add_argument("--config", default=default, help=f"YAML config (default: {default})")


def cmd_prepare(a) -> int:
    from .config import load_config
    from .data import prepare_data
    m = prepare_data(a.source, load_config(a.config))
    print(json.dumps({k: v for k, v in m.items() if k != "documents"}, indent=2))
    print("OK: data prepared under data/raw and data/processed")
    return 0


def cmd_validate(a) -> int:
    from .chunking import chunk_corpus, validate_chunks
    from .config import load_config
    from .data import load_dataset, validate_dataset
    cfg = load_config(a.config)
    ds = load_dataset(cfg)
    rep = validate_dataset(ds)
    chunks = chunk_corpus(ds.documents, cfg["chunking"])
    rep["n_chunks"] = len(chunks)
    rep["chunk_offset_violations"] = validate_chunks(chunks, ds.documents)
    rep["ok"] = rep["ok"] and rep["chunk_offset_violations"] == 0
    print(json.dumps(rep, indent=2))
    print("VALIDATION OK" if rep["ok"] else "VALIDATION FAILED")
    return 0 if rep["ok"] else 1


def cmd_build_index(a) -> int:
    from .config import index_fingerprint, load_config, resolve_path
    from .pipeline import Pipeline
    cfg = load_config(a.config)
    t0 = time.time()
    pipe = Pipeline.from_config(cfg)
    out = resolve_path(cfg["output"]["artifacts_dir"]) / "index" / index_fingerprint(cfg)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "chunks.jsonl", "w", encoding="utf-8") as f:
        for c in pipe.index.chunks:
            f.write(json.dumps({"chunk_id": c.chunk_id, "document_id": c.document_id,
                                "start_offset": c.start, "end_offset": c.end, "n_chars": c.end - c.start}) + "\n")
    lens = [c.end - c.start for c in pipe.index.chunks]
    stats = {"config": cfg["name"], "fingerprint": index_fingerprint(cfg), "n_documents": len(pipe.documents),
             "n_chunks": len(lens), "mean_chunk_chars": sum(lens) / max(1, len(lens)), "max_chunk_chars": max(lens),
             "vocab_size": len(pipe.index.bm25.postings), "dense": pipe.index.emb is not None,
             "seconds": round(time.time() - t0, 2)}
    (out / "stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))
    print(f"OK: index artifacts in {out}")
    return 0


def print_result(res, as_json: bool) -> None:
    from .pipeline import DISCLAIMER
    if as_json:
        print(json.dumps(res.to_dict(), indent=2))
        return
    print(f"Query: {res.query}")
    if res.document_filter:
        print(f"Restricted to contract: {res.document_filter}")
    if res.abstention_reason == "contract_not_identified":
        print("ABSTAINED: the question does not name a contract, so no contract was assumed.")
        print("Name it in the query (\"Consider the <Agreement> between <A> and <B>; <question>\") "
              "or pass --document. Closest matches:")
        for c in res.contract_candidates:
            print(f"  - {c}")
        print(f"\n{DISCLAIMER}")
        return
    expanded = {t: w for t, w in res.ranking_terms.items() if w < 1.0}
    if expanded:
        print("Ranking-query expansion terms (weight): " + ", ".join(f"{t}({w:g})" for t, w in expanded.items()))
    if res.abstained:
        print(f"ABSTAINED: no sufficiently relevant evidence found "
              f"(reason={res.abstention_reason}; {res.signal_text()})")
    else:
        print(f"Answered with {len(res.passages)} passage(s)  ({res.signal_text()})")
    for p in res.passages:
        rr = (f"  rerank={p['rerank_score']:.4f} (bm25 rank {p['bm25_rank']})"
              if p.get("rerank_score") is not None else "")
        print(f"\n#{p['rank']}  score={p['score']:.4f}{rr}  document={p['document_id']}  "
              f"offsets=[{p['start_offset']}, {p['end_offset']})")
        print("    " + p["text"].strip().replace("\n", "\n    "))
    print(f"\n{DISCLAIMER}")


def cmd_search(a) -> int:
    from .pipeline import Pipeline, PipelineError
    try:
        pipe = Pipeline.from_config(a.config)
        res = pipe.search(a.query, top_k=a.top_k, document=a.document)
    except (PipelineError, FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print_result(res, a.json)
    return 0


def cmd_show_span(a) -> int:
    from .pipeline import Pipeline, PipelineError
    try:
        pipe = Pipeline.from_config(a.config)
        doc = pipe.resolve_document(a.document)
    except PipelineError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    text = pipe.documents[doc]
    if not 0 <= a.start < a.end <= len(text):
        print(f"error: span [{a.start}, {a.end}) outside document length {len(text)}", file=sys.stderr)
        return 2
    print(f"document={doc}  span=[{a.start}, {a.end})  chars={a.end - a.start}")
    print(text[a.start:a.end])
    return 0


def cmd_evaluate(a) -> int:
    from .config import load_config, resolve_path
    from .data import load_dataset
    from .evaluation import evaluate, format_summary, record_test_run, write_results
    cfg = load_config(a.config)
    if a.split == "test" and not a.final_test:
        print("error: evaluating the held-out TEST split requires --final-test "
              "(only after the final config is selected; each run is logged).", file=sys.stderr)
        return 2
    calibrate = None if a.split == "train" else False
    if a.no_calibrate:
        calibrate = False
    ds = load_dataset(cfg)
    res = evaluate(cfg, ds, a.split, calibrate_on_train=calibrate, allow_test=a.final_test)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = a.out or f"{cfg['output']['artifacts_dir']}/eval/{cfg['name']}_{a.split}_{stamp}"
    out = write_results(res, out_dir)
    if a.split == "test":
        n = record_test_run(cfg, out, cfg["output"]["artifacts_dir"])
        print(f"[test-run #{n} recorded in {resolve_path(cfg['output']['artifacts_dir']) / 'test_runs.jsonl'}]")
    print(format_summary(res))
    print(f"OK: results written to {out}")
    if a.split == "train" and res["calibration"] and a.write_threshold:
        _write_threshold(a.config, res["calibration"]["threshold"], res["calibration"].get("doc_threshold"))
    return 0


def _write_threshold(config_path: str, thr: float, doc_thr: float | None = None) -> None:
    import yaml
    from .config import resolve_path
    p = resolve_path(config_path)
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    raw.setdefault("abstention", {})["threshold"] = float(thr)
    if doc_thr is not None:
        raw["abstention"]["doc_threshold"] = float(doc_thr)
    p.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    extra = f" and doc_threshold {doc_thr:.6f}" if doc_thr is not None else ""
    print(f"Wrote train-calibrated threshold {thr:.6f}{extra} into {p}")


def cmd_improve(a) -> int:
    from .config import load_config
    from .data import load_dataset, validate_dataset
    from .improvement_loop import load_loop_spec, run_loop
    cfg = load_config(a.config)
    ds = load_dataset(cfg)
    rep = validate_dataset(ds)
    if not rep["ok"]:
        print("error: data validation failed; run validate-data first", file=sys.stderr)
        return 1
    spec = load_loop_spec(a.spec)
    run = a.run_name or dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = f"{cfg['output']['artifacts_dir']}/loop/{run}"
    from .config import resolve_path
    logf = resolve_path(run_dir)
    logf.mkdir(parents=True, exist_ok=True)
    fh = open(logf / "loop.log", "w", encoding="utf-8")

    def log(msg: str) -> None:
        print(msg, flush=True)
        fh.write(msg + "\n")
        fh.flush()
    try:
        s = run_loop(cfg, ds, spec, run_dir, log=log, max_iterations=a.max_iterations)
    finally:
        fh.close()
    return 0 if s["met_min_iterations"] else 1


def cmd_error_analysis(a) -> int:
    from .config import load_config, resolve_path
    from .data import load_dataset
    from .diagnostics import error_analysis
    from .evaluation import evaluate
    cfg = load_config(a.config)
    ds = load_dataset(cfg)
    res = evaluate(cfg, ds, "train")  # train only: error analysis drives decisions
    out = a.out or f"{cfg['output']['artifacts_dir']}/error_analysis/{cfg['name']}"
    s = error_analysis(res["per_query"], res["config"], ds.documents, out, cfg["name"], per_category=a.per_category)
    print(json.dumps(s, indent=2))
    print(f"OK: see {resolve_path(out) / 'error_analysis.md'} and failures.jsonl")
    return 0


def cmd_demo_check(a) -> int:
    from .demo_check import format_report, run_demo_check
    from .pipeline import Pipeline
    res = run_demo_check(Pipeline.from_config(a.config, overrides=None), top_k=a.top_k, n_types=a.n_types)
    print(format_report(res))
    return 0 if res["summary"]["C"][0] == res["summary"]["C"][1] else 1


def cmd_compare(a) -> int:
    from .compare import compare, format_comparison
    c = compare(a.runs, a.k, a.extra_k, a.qids or [])
    print(format_comparison(c))
    if a.out:
        from .config import resolve_path
        p = resolve_path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(c, indent=2), encoding="utf-8")
        print(f"OK: comparison written to {p}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m src.cli",
                                description="Contract Intelligence Assistant (LegalBench-RAG-mini, CUAD)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("prepare-data", help="copy cuad.json + referenced contracts into data/raw")
    s.add_argument("--source", required=True, help="path to the downloaded LegalBench-RAG root")
    _add_config(s, "configs/baseline.yaml")
    s.set_defaults(func=cmd_prepare)

    s = sub.add_parser("validate-data", help="check mini selection, split, gold offsets, negatives, chunks")
    _add_config(s, "configs/baseline.yaml")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("build-index", help="chunk + index (and dense-embed if configured); write stats")
    _add_config(s)
    s.set_defaults(func=cmd_build_index)

    s = sub.add_parser("search", help="search the indexed contracts")
    s.add_argument("--query", "-q", required=True, help="natural-language question")
    s.add_argument("--top-k", "-k", type=int, default=5, help="number of passages to return (default 5)")
    s.add_argument("--json", action="store_true", help="print machine-readable JSON")
    s.add_argument("--document", "-d", default=None,
                   help="restrict to one contract (exact document_id or unique substring, e.g. PapaJohns)")
    _add_config(s)
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("show-span", help="print document[start:end] from the original source text")
    s.add_argument("--document", "-d", required=True, help="exact document_id or unique substring")
    s.add_argument("--start", type=int, required=True)
    s.add_argument("--end", type=int, required=True)
    _add_config(s)
    s.set_defaults(func=cmd_show_span)

    s = sub.add_parser("evaluate", help="evaluate a config on train (default) or, with --final-test, test")
    _add_config(s)
    s.add_argument("--split", choices=["train", "test"], default="train")
    s.add_argument("--final-test", action="store_true", help="required to touch the held-out test split")
    s.add_argument("--no-calibrate", action="store_true", help="use the threshold stored in the config")
    s.add_argument("--write-threshold", action="store_true",
                   help="(train only) write the calibrated threshold back into --config")
    s.add_argument("--out", default=None, help="output directory")
    s.set_defaults(func=cmd_evaluate)

    s = sub.add_parser("improve", help="run the train-only improvement loop")
    _add_config(s, "configs/baseline.yaml")
    s.add_argument("--spec", default="configs/loop.yaml")
    s.add_argument("--run-name", default=None)
    s.add_argument("--max-iterations", type=int, default=None)
    s.set_defaults(func=cmd_improve)

    s = sub.add_parser("error-analysis", help="categorised failures on TRAIN for a config")
    _add_config(s)
    s.add_argument("--out", default=None)
    s.add_argument("--per-category", type=int, default=4)
    s.set_defaults(func=cmd_error_analysis)
    s = sub.add_parser("demo-check", help="PASS/FAIL battery: real train queries, negatives, bad inputs")
    _add_config(s)
    s.add_argument("--top-k", "-k", type=int, default=5)
    s.add_argument("--n-types", type=int, default=10, help="number of question types to sample")
    s.set_defaults(func=cmd_demo_check)

    s = sub.add_parser("compare", help="compare saved evaluate runs (metrics.json + per_query.jsonl)")
    s.add_argument("runs", nargs="+", help="evaluation output directories; the first is the reference")
    s.add_argument("--k", type=int, nargs="+", default=[1, 2, 5], help="k values read from metrics.json")
    s.add_argument("--extra-k", type=int, nargs="+", default=[10],
                   help="k values (<= 10) recomputed from the stored top-10 passages")
    s.add_argument("--qids", nargs="*", default=None, help="query ids for the per-case rank table")
    s.add_argument("--out", default=None, help="optional JSON output path")
    s.set_defaults(func=cmd_compare)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
