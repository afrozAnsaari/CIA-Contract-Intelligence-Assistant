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


DUAL = {"enabled": True, "signal": "doc_and_chunk", "threshold": 0.3, "doc_threshold": 0.5}


def test_dual_rule_each_part_and_equality():
    ok = {"doc_bm25_norm": 0.5, "chunk_bm25_norm": 0.3}  # both exactly at threshold => answer
    assert not decide(2, ok, DUAL).abstained
    d = decide(2, {"doc_bm25_norm": 0.49, "chunk_bm25_norm": 0.9}, DUAL)
    assert d.abstained and d.reason == "below_doc_threshold"
    d = decide(2, {"doc_bm25_norm": 0.9, "chunk_bm25_norm": 0.29}, DUAL)
    assert d.abstained and d.reason == "below_threshold"
    assert decide(0, ok, DUAL).reason == "no_candidates"
    with pytest.raises(KeyError):
        decide(2, {"chunk_bm25_norm": 0.9}, DUAL)


def test_calibrate_dual_needs_both_dimensions():
    from src.abstention import calibrate_dual
    # answerable: strong doc + strong chunk; negatives: weak doc (fake contract) OR weak chunk (absent topic)
    pos = [(0.8, 0.5), (0.7, 0.6), (0.9, 0.4)]
    neg = [(0.2, 0.6), (0.3, 0.5), (0.8, 0.1), (0.9, 0.05)]
    r = calibrate_dual(pos, neg)
    assert r["balanced_accuracy"] == 1.0
    assert 0.3 < r["doc_threshold"] <= 0.7 and 0.1 < r["threshold"] <= 0.4
    # a single chunk threshold cannot separate this data
    assert calibrate([c for _, c in pos], [c for _, c in neg])["balanced_accuracy"] < 1.0


def test_dual_requires_routing():
    from src.config import load_config
    with pytest.raises(ValueError):
        load_config(None, {"abstention.signal": "doc_and_chunk"})


def test_dual_calibration_through_evaluation(tiny):
    cfg, ds = tiny
    c = apply_overrides(cfg, {"query.mode": "split", "query.chunk_query": "question",
                              "retrieval.doc_routing.enabled": True, "abstention.signal": "doc_and_chunk"})
    res = evaluate(c, ds, "train")
    assert res["calibration"]["signal"] == "doc_and_chunk"
    assert res["config"]["abstention"]["doc_threshold"] == res["calibration"]["doc_threshold"]
    row = res["per_query"][0]
    assert row["doc_signal_value"] is not None and row["doc_threshold"] is not None
    r = Pipeline(res["config"], ds.documents).search("What does the agreement say about zorblax obligations?")
    assert "doc_bm25_norm=" in r.signal_text()


def test_full_query_signal_decoupled_from_ranking(tiny):
    cfg, ds = tiny
    q = "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What is the governing law?"
    full = Pipeline(apply_overrides(cfg, {"query.mode": "split", "retrieval.doc_routing.enabled": True}),
                    ds.documents).retrieve(q, 5)
    assert full.signals["chunk_full_bm25_norm"] == full.signals["chunk_bm25_norm"]
    qo = Pipeline(apply_overrides(cfg, {"query.mode": "split", "query.chunk_query": "question",
                                        "retrieval.doc_routing.enabled": True,
                                        "abstention.signal": "chunk_full_bm25_norm"}), ds.documents)
    out = qo.retrieve(q, 5)
    assert out.signals["chunk_full_bm25_norm"] == pytest.approx(full.signals["chunk_bm25_norm"])
    assert out.signals["chunk_bm25_norm"] != out.signals["chunk_full_bm25_norm"]
    assert qo.search(q, 3).signal == "chunk_full_bm25_norm"


def test_stopword_only_query_abstains(tiny):
    cfg, ds = tiny
    r = Pipeline(cfg, ds.documents).search("the of and", 3)
    assert r.abstained and r.abstention_reason == "no_candidates" and r.passages == []


IQ = {"enabled": True, "signal": "identity_and_question", "threshold": 0.2, "doc_threshold": 0.4}


def test_identity_and_question_rule():
    ok = {"preamble_bm25_norm": 0.4, "chunk_bm25_norm": 0.2}
    assert not decide(2, ok, IQ).abstained  # equality on both parts answers
    d = decide(2, {"preamble_bm25_norm": 0.39, "chunk_bm25_norm": 0.9}, IQ)
    assert d.abstained and d.reason == "below_doc_threshold"
    d = decide(2, {"preamble_bm25_norm": 0.9, "chunk_bm25_norm": 0.19}, IQ)
    assert d.abstained and d.reason == "below_threshold"


def test_identity_and_question_requires_split_routing():
    from src.config import load_config
    with pytest.raises(ValueError):
        load_config(None, {"abstention.signal": "identity_and_question"})


def test_preamble_signal_identity_explicit_document(tiny):
    cfg, ds = tiny
    c = apply_overrides(cfg, {"query.mode": "split", "query.chunk_query": "question",
                              "retrieval.doc_routing.enabled": True})
    p = Pipeline(c, ds.documents)
    named = p.retrieve("Consider the License Agreement between AlphaCo Inc. and Gamma LLC; governing law?", 3)
    fake = p.retrieve("Consider the License Agreement between Zorblax Ltd and Quintessor Plc; governing law?", 3)
    assert named.signals["preamble_bm25_norm"] > fake.signals["preamble_bm25_norm"]
    explicit = p.retrieve("governing law", 3, document_id="cuad/AlphaCo_License Agreement.txt")
    assert explicit.signals["preamble_bm25_norm"] == 1.0  # identity given by the user
