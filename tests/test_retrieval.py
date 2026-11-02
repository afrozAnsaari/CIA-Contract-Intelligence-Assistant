import math

import pytest

from src.config import apply_overrides
from src.pipeline import Pipeline, PipelineError
from src.retrieval import BM25, _largest_uncovered


def test_bm25_hand_computed():
    docs = [["a", "b"], ["a", "a", "c"], ["c"]]
    bm = BM25(docs, k1=1.5, b=0.75)
    avgdl = 2.0
    idf_a = math.log(1 + (3 - 2 + 0.5) / (2 + 0.5))
    norm1 = 1.5 * (1 - 0.75 + 0.75 * 3 / avgdl)
    expected = idf_a * 2 * 2.5 / (2 + norm1)
    assert bm.scores(["a"])[1] == pytest.approx(expected)
    assert bm.scores(["zzz"]).sum() == 0
    assert bm.upper_bound(["a", "a"]) == pytest.approx(idf_a * 2.5)  # unique terms only
    assert bm.upper_bound(["zzz"]) > 0  # OOV counts in the denominator


def test_ranking_sorted_offsets_valid_topk(tiny):
    cfg, ds = tiny
    p = Pipeline(cfg, ds.documents)
    out = p.retrieve("sublicense Licensed Technology consent", 3)
    assert 1 <= len(out.passages) <= 3
    scores = [x.score for x in out.passages]
    assert scores == sorted(scores, reverse=True)
    assert [x.rank for x in out.passages] == list(range(1, len(out.passages) + 1))
    for x in out.passages:
        assert ds.documents[x.document_id][x.start_offset:x.end_offset] == x.text
    assert "sublicense" in out.passages[0].text


def test_deterministic_and_tie_order(tiny):
    cfg, ds = tiny
    p = Pipeline(cfg, ds.documents)
    a = [(x.document_id, x.start_offset) for x in p.retrieve("agreement", 10).passages]
    b = [(x.document_id, x.start_offset) for x in p.retrieve("agreement", 10).passages]
    assert a == b
    out = p.retrieve("agreement", 10).passages
    for x, y in zip(out, out[1:]):  # equal scores => ascending chunk id
        if x.score == y.score:
            assert x.chunk_id < y.chunk_id


def test_empty_query_fails_gracefully(tiny):
    cfg, ds = tiny
    p = Pipeline(cfg, ds.documents)
    with pytest.raises(PipelineError):
        p.search("   ")
    with pytest.raises(PipelineError):
        p.search("x", top_k=0)


def test_missing_data_fails_gracefully(tiny, tmp_path):
    cfg, _ = tiny
    bad = apply_overrides(cfg, {"data.raw_dir": str(tmp_path / "nope")})
    with pytest.raises(PipelineError):
        Pipeline.from_config(bad)


def test_config_changes_behavior(tiny):
    cfg, ds = tiny
    small = Pipeline(apply_overrides(cfg, {"chunking.max_chars": 80, "chunking.overlap_chars": 0}), ds.documents)
    big = Pipeline(apply_overrides(cfg, {"chunking.max_chars": 400, "chunking.overlap_chars": 0}), ds.documents)
    assert len(small.index.chunks) > len(big.index.chunks)
    stem = Pipeline(apply_overrides(cfg, {"text.stemming": True}), ds.documents)
    assert stem.retrieve("sublicensing", 1).passages  # stem matches 'sublicense'


def test_doc_routing_restricts_documents(tiny):
    cfg, ds = tiny
    c = apply_overrides(cfg, {"query.mode": "split", "retrieval.doc_routing.enabled": True,
                              "retrieval.doc_routing.top_n_docs": 1})
    out = Pipeline(c, ds.documents).retrieve(
        "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; What is the governing law?", 10)
    assert {x.document_id for x in out.passages} <= {"cuad/BetaInc_Supply Agreement.txt"}
    assert out.routed_documents == ["cuad/BetaInc_Supply Agreement.txt"]
    assert "doc_bm25_norm" in out.signals


@pytest.mark.parametrize("policy", ["skip", "trim"])
def test_overlap_policy_no_overlap(tiny, policy):
    cfg, ds = tiny
    c = apply_overrides(cfg, {"chunking.max_chars": 120, "chunking.overlap_chars": 60,
                              "retrieval.overlap_policy": policy, "retrieval.min_trimmed_chars": 1})
    out = Pipeline(c, ds.documents).retrieve("agreement licensee supplier buyer", 16).passages
    for i, a in enumerate(out):
        for b in out[i + 1:]:
            if a.document_id == b.document_id:
                assert a.end_offset <= b.start_offset or b.end_offset <= a.start_offset


def test_largest_uncovered():
    assert _largest_uncovered(0, 100, [(0, 30)]) == (30, 100)
    assert _largest_uncovered(0, 100, [(40, 60)]) == (60, 100) or _largest_uncovered(0, 100, [(40, 60)]) == (0, 40)
    assert _largest_uncovered(0, 100, [(0, 100)]) == (0, 0)


class FakeEncoder:
    """Deterministic bag-of-words hashing encoder (stands in for sentence-transformers)."""

    def encode(self, texts):
        import numpy as np
        out = np.zeros((len(texts), 64), dtype=np.float32)
        for i, t in enumerate(texts):
            for w in t.lower().split():
                out[i, hash(w) % 64] += 1.0
        n = np.linalg.norm(out, axis=1, keepdims=True)
        return out / np.where(n == 0, 1, n)


@pytest.mark.parametrize("method", ["dense", "hybrid"])
def test_dense_and_hybrid_paths_with_fake_encoder(tiny, method):
    from src.retrieval import Index
    cfg, ds = tiny
    c = apply_overrides(cfg, {"retrieval.method": method, "abstention.signal": "dense_max_cos"})
    idx = Index(c, ds.documents, encoder=FakeEncoder(), use_cache=False)
    out = idx.retrieve("Licensee shall not sublicense the Licensed Technology", 4)
    assert out.passages and "dense_max_cos" in out.signals and "chunk_bm25_norm" in out.signals
    s = [p.score for p in out.passages]
    assert s == sorted(s, reverse=True)
    for p in out.passages:
        assert ds.documents[p.document_id][p.start_offset:p.end_offset] == p.text


# --- contract identity (E2 regression) -------------------------------------------------
SPLIT = {"query.mode": "split", "query.chunk_query": "question", "retrieval.doc_routing.enabled": True,
         "abstention.signal": "chunk_full_bm25_norm", "abstention.threshold": 0.0}


def test_unnamed_contract_is_not_silently_routed(tiny):
    cfg, ds = tiny
    p = Pipeline(apply_overrides(cfg, {**SPLIT, "query.require_contract": True}), ds.documents)
    r = p.search("What is the governing law for this contract?", 3)
    assert r.abstained and r.abstention_reason == "contract_not_identified" and r.passages == []
    assert r.contract_candidates and set(r.contract_candidates) <= set(ds.documents)
    named = p.search("Consider the License Agreement between AlphaCo Inc. and Gamma LLC; "
                     "What is the governing law for this contract?", 3)
    assert not named.abstained and named.passages  # named contracts unaffected


def test_require_contract_off_keeps_old_routing(tiny):
    cfg, ds = tiny
    out = Pipeline(apply_overrides(cfg, SPLIT), ds.documents).retrieve("What is the governing law?", 3)
    assert not out.unresolved_contract and out.routed_documents


def test_document_filter_and_resolution(tiny):
    cfg, ds = tiny
    p = Pipeline(apply_overrides(cfg, {**SPLIT, "query.require_contract": True}), ds.documents)
    r = p.search("What is the governing law for this contract?", 5, document="AlphaCo")
    assert not r.abstained and r.document_filter == "cuad/AlphaCo_License Agreement.txt"
    assert r.passages and all(x["document_id"] == r.document_filter for x in r.passages)
    with pytest.raises(PipelineError):
        p.search("governing law", 3, document="NoSuchContract")
    with pytest.raises(PipelineError):
        p.search("governing law", 3, document="Agreement")  # ambiguous substring


def test_evaluation_records_contract_not_identified(tiny):
    from src.evaluation import evaluate
    cfg, ds = tiny
    res = evaluate(apply_overrides(cfg, {**SPLIT, "query.require_contract": True}), ds, "train")
    neg = [r for r in res["per_query"] if not r["answerable"]]
    assert neg and all(r["abstained"] for r in neg)
    assert {r["abstention_reason"] for r in neg} == {"contract_not_identified"}  # fixture negatives name no contract
