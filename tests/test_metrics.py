import pytest

from src.metrics import (abstention_metrics, f1, mean_metrics, merge_intervals, metrics_at_k, precision_recall,
                         reference_precision_recall)

G = [("d", 100, 200)]


def test_exact_match():
    assert precision_recall([("d", 100, 200)], G) == (1.0, 1.0)


def test_partial_coverage():
    p, r = precision_recall([("d", 150, 200)], G)
    assert p == 1.0 and r == 0.5


def test_irrelevant_extra_text():
    p, r = precision_recall([("d", 0, 400)], G)
    assert p == pytest.approx(0.25) and r == 1.0


def test_wrong_document():
    assert precision_recall([("other", 100, 200)], G) == (0.0, 0.0)


def test_multiple_gold_spans():
    gold = [("d", 0, 100), ("e", 0, 100)]
    p, r = precision_recall([("d", 0, 100)], gold)
    assert p == 1.0 and r == 0.5
    p, r = precision_recall([("d", 50, 100), ("e", 0, 100)], gold)
    assert p == 1.0 and r == 0.75


def test_overlapping_and_duplicate_results_not_double_counted():
    p, r = precision_recall([("d", 100, 200), ("d", 100, 200), ("d", 150, 250)], G)
    assert p == pytest.approx(100 / 150) and r == 1.0
    rp, rr = reference_precision_recall([("d", 100, 200), ("d", 100, 200)], G)
    assert rr == 2.0  # the pairwise reference variant double counts duplicates


def test_reference_equals_set_based_when_disjoint():
    ret = [("d", 0, 120), ("d", 150, 260), ("x", 0, 50)]
    gold = [("d", 100, 200), ("d", 240, 300)]
    assert precision_recall(ret, gold) == pytest.approx(reference_precision_recall(ret, gold))


def test_empty_retrieval():
    assert precision_recall([], G) == (0.0, 0.0)
    m = metrics_at_k([], G, [1, 5])
    assert m["precision@1"] == 0 and m["recall@5"] == 0 and m["f1@5"] == 0


def test_k_cutoffs():
    ret = [("x", 0, 10), ("d", 100, 150), ("d", 150, 200)]
    m = metrics_at_k(ret, G, [1, 2, 3, 10])
    assert m["recall@1"] == 0 and m["recall@2"] == 0.5 and m["recall@3"] == 1.0 and m["recall@10"] == 1.0
    assert m["precision@2"] == pytest.approx(50 / 60)
    assert m["f1@3"] == pytest.approx(f1(100 / 110, 1.0))


def test_aggregation_macro_mean_with_n():
    rows = [metrics_at_k([("d", 100, 200)], G, [1]), metrics_at_k([], G, [1])]
    agg = mean_metrics(rows)
    assert agg["n"] == 2 and agg["recall@1"] == 0.5 and agg["precision@1"] == 0.5
    assert mean_metrics([]) == {"n": 0}


def test_merge_intervals():
    assert merge_intervals([(5, 10), (0, 3), (3, 4), (8, 12), (20, 20)]) == [(0, 4), (5, 12)]


def test_abstention_metrics_denominators():
    m = abstention_metrics([False, True, False, False], [True, True, False])
    assert m["false_abstention_rate"] == 0.25 and m["correct_abstention_rate"] == pytest.approx(2 / 3)
    assert m["failure_to_abstain_rate"] == pytest.approx(1 / 3)
    assert m["balanced_accuracy"] == pytest.approx(0.5 * (0.75 + 2 / 3))
    assert abstention_metrics([], [])["balanced_accuracy"] is None
