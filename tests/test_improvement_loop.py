import json

import yaml

from src.config import apply_overrides, load_config
from src.improvement_loop import compare, resolve_changes, run_loop

SPEC = {
    "protocol": {"primary_metric": "retrieval.f1@5", "min_improvement": 0.0, "max_iterations": 6,
                 "min_iterations": 5,
                 "guardrails": [{"metric": "retrieval.recall@5", "max_drop": 0.05},
                                {"metric": "offset_errors", "must_equal": 0}]},
    "candidates": [
        {"id": "c_small", "tags": ["irrelevant_extra"], "hypothesis": "h", "changes": {"chunking.max_chars": 120}},
        {"id": "c_route", "tags": ["wrong_document"], "hypothesis": "h",
         "changes": {"query.mode": "split", "retrieval.doc_routing.enabled": True}},
        {"id": "c_stem", "tags": [], "hypothesis": "h", "changes": {"text.stemming": True}},
        {"id": "c_overlap", "tags": [], "hypothesis": "h",
         "changes": {"chunking.overlap_chars": {"frac_of": "chunking.max_chars", "frac": 0.3}}},
        {"id": "c_trim", "tags": [], "hypothesis": "h", "changes": {"retrieval.overlap_policy": "trim"}},
        {"id": "c_bad", "tags": [], "hypothesis": "invalid", "changes": {"abstention.signal": "dense_max_cos"}},
        {"id": "c_big", "tags": [], "hypothesis": "h", "changes": {"chunking.max_chars": 400}},
        {"id": "c_dense", "requires": "dense", "tags": [], "hypothesis": "h", "changes": {"retrieval.method": "dense"}},
    ],
}


def _run(tiny, tmp_path):
    cfg, ds = tiny
    neg_path = cfg["data"]["unanswerable_path"]
    before = open(neg_path, "rb").read()
    s = run_loop(cfg, ds, SPEC, tmp_path / "loop", log=lambda m: None)
    assert open(neg_path, "rb").read() == before  # frozen set untouched
    rows = [json.loads(x) for x in open(tmp_path / "loop" / "iterations.jsonl")]
    return cfg, ds, s, rows


def test_loop_runs_logs_and_preserves_baseline(tiny, tmp_path):
    cfg, ds, s, rows = _run(tiny, tmp_path)
    assert rows[0]["candidate_id"] == "baseline" and rows[0]["decision"] == "accepted"
    evaluated = [r for r in rows if r.get("iteration")]
    assert len(evaluated) >= 5 and s["met_min_iterations"]
    assert {r["decision"] for r in evaluated} <= {"accepted", "rejected"}
    assert any(r["decision"] == "skipped" for r in rows)  # invalid candidate is logged, not run
    for r in evaluated:
        for key in ("candidate_id", "hypothesis", "changes", "metrics", "guardrails", "decision", "reason",
                    "timestamp", "proposer"):
            assert key in r
    assert (tmp_path / "loop" / "iter00_baseline" / "metrics.json").exists()


def test_loop_uses_train_only(tiny, tmp_path):
    cfg, ds, s, rows = _run(tiny, tmp_path)
    n_train = len(ds.split("train"))
    n_neg_train = len(ds.split("train", False))
    for r in rows:
        if r.get("metrics"):
            assert r["metrics"]["n_train_answerable"] == n_train
            assert r["metrics"]["n_train_unanswerable"] == n_neg_train
    per_q = [json.loads(x) for x in open(tmp_path / "loop" / "iter00_baseline" / "per_query.jsonl")]
    assert {r["split"] for r in per_q} == {"train"}


def test_rejected_never_overwrites_accepted(tiny, tmp_path):
    cfg, ds, s, rows = _run(tiny, tmp_path)
    accepted = yaml.safe_load(open(tmp_path / "loop" / "accepted_config.yaml"))
    last_acc = [r for r in rows if r["decision"] == "accepted"][-1]
    assert accepted["name"] == (cfg["name"] if last_acc["candidate_id"] == "baseline" else last_acc["candidate_id"])
    assert s["accepted_candidate"] == last_acc["candidate_id"]


def test_reproducible(tiny, tmp_path):
    cfg, ds = tiny
    a = run_loop(cfg, ds, SPEC, tmp_path / "a", log=lambda m: None)
    b = run_loop(cfg, ds, SPEC, tmp_path / "b", log=lambda m: None)
    strip = lambda d: {k: v for k, v in d.items() if k not in {"run_dir", "finished"}}  # noqa: E731
    assert strip(a) == strip(b)


def test_compare_rule():
    proto = {"primary_metric": "retrieval.f1@5", "min_improvement": 0.01,
             "guardrails": [{"metric": "retrieval.recall@5", "max_drop": 0.05}, {"metric": "offset_errors", "must_equal": 0}]}
    acc = {"retrieval": {"f1@5": 0.30, "recall@5": 0.80}, "offset_errors": 0}
    ok, *_ = compare({"retrieval": {"f1@5": 0.35, "recall@5": 0.76}, "offset_errors": 0}, acc, proto)
    assert ok
    ok, reason, *_ = compare({"retrieval": {"f1@5": 0.35, "recall@5": 0.70}, "offset_errors": 0}, acc, proto)
    assert not ok and "guardrail" in reason
    ok, reason, *_ = compare({"retrieval": {"f1@5": 0.305, "recall@5": 0.9}, "offset_errors": 0}, acc, proto)
    assert not ok and "min_improvement" in reason
    ok, *_ = compare({"retrieval": {"f1@5": 0.5, "recall@5": 0.9}, "offset_errors": 1}, acc, proto)
    assert not ok


def test_resolve_changes():
    cfg = load_config(None)
    assert resolve_changes(cfg, {"chunking.overlap_chars": {"frac_of": "chunking.max_chars", "frac": 0.3}}) == \
        {"chunking.overlap_chars": 300}
    assert apply_overrides(cfg, {"a.b": 1})["a"]["b"] == 1 and "a" not in cfg


def test_committed_loop_spec_is_valid():
    from src.improvement_loop import load_loop_spec
    spec = load_loop_spec("configs/loop.yaml")
    assert spec["protocol"]["min_iterations"] >= 5
    assert sum(1 for c in spec["candidates"] if c.get("requires") != "dense") >= 5
