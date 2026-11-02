import pytest

from src.abstention import calibrate, decide
from src.config import apply_overrides
from src.evaluation import evaluate
from src.pipeline import Pipeline

A = {"enabled": True, "signal": "chunk_bm25_norm", "threshold": 0.3}


def test_threshold_equality_answers():
    assert not decide(3, {"chunk_bm25_norm": 0.3}, A).abstained
    assert decide(3, {"chunk_bm25_norm": 0.2999}, A).abstained


def test_no_candidates_abstains_even_if_disabled():
    d = decide(0, {"chunk_bm25_norm": 0.9}, {**A, "enabled": False})
    assert d.abstained and d.reason == "no_candidates"


def test_method_specific_signal():
    cfg = {"enabled": True, "signal": "dense_max_cos", "threshold": 0.5}
    assert not decide(1, {"chunk_bm25_norm": 0.0, "dense_max_cos": 0.6}, cfg).abstained
    with pytest.raises(KeyError):
        decide(1, {"chunk_bm25_norm": 0.9}, cfg)


def test_calibrate_separable_and_ties():
    r = calibrate([0.5, 0.6, 0.7], [0.1, 0.2])
    assert r["balanced_accuracy"] == 1.0 and 0.2 < r["threshold"] <= 0.5
    assert r["threshold"] == pytest.approx(0.35)  # smallest best = midpoint(0.2, 0.5)
    r2 = calibrate([0.5], [])
    assert r2["threshold"] == 0.5  # answer all
    assert calibrate([], [])["threshold"] == 0.0


def test_strong_answerable_returns_evidence(tiny):
    cfg, ds = tiny
    p = Pipeline(cfg, ds.documents)
    r = p.search("Licensee shall not sublicense the Licensed Technology without prior written consent", 3)
    assert not r.abstained and r.passages


def test_unanswerable_rejected(tiny):
    cfg, ds = tiny
    r = Pipeline(cfg, ds.documents).search("What does the agreement say about zorblax obligations?", 3)
    assert r.abstained


def test_false_abstention_and_failure_to_abstain_measured(tiny):
    cfg, ds = tiny
    # Absurdly high threshold => every answerable query is a false abstention.
    hi = apply_overrides(cfg, {"abstention.threshold": 0.99})
    res = evaluate(hi, ds, "train", calibrate_on_train=False)
    assert res["abstention"]["false_abstention_rate"] == 1.0
    assert res["retrieval_with_abstention"]["recall@5"] == 0.0
    assert res["retrieval"]["recall@5"] > 0  # raw retrieval is still scored separately
    # Threshold 0 => weakly matched negatives ("agreement", "obligations") are not rejected.
    lo = apply_overrides(cfg, {"abstention.threshold": 0.0})
    res = evaluate(lo, ds, "train", calibrate_on_train=False)
    assert res["abstention"]["failure_to_abstain_rate"] > 0
