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


# --- document filter must not pass vacuously ---------------------------------------------
def _split_pipe(cfg, ds, **extra):
    return Pipeline(apply_overrides(cfg, {**SPLIT, "query.require_contract": True, **extra}), ds.documents)


def test_document_filter_alias_and_full_id_nonempty(tiny):
    cfg, ds = tiny
    p = _split_pipe(cfg, ds)
    q = "What is the governing law for this contract?"
    by_alias = p.search(q, 5, document="AlphaCo")
    by_id = p.search(q, 5, document="cuad/AlphaCo_License Agreement.txt")
    assert by_alias.passages, "known answerable (contract, question) must return evidence"
    assert by_alias.passages == by_id.passages
    assert all(x["document_id"] == "cuad/AlphaCo_License Agreement.txt" for x in by_alias.passages)
    assert any("governed by the laws" in x["text"] for x in by_alias.passages)


def test_document_filter_with_no_relevant_passages_returns_nothing_else(tiny):
    """Zero results ARE the expected behaviour here (the contract has no insurance clause):
    the test asserts that nothing from any other contract leaks in, not that evidence exists."""
    cfg, ds = tiny
    r = _split_pipe(cfg, ds).search("What are the insurance requirements?", 5, document="AlphaCo")
    # AlphaCo has no insurance clause: either abstain or only AlphaCo passages, never BetaInc's.
    assert all(x["document_id"] == "cuad/AlphaCo_License Agreement.txt" for x in r.passages)


def test_document_filter_overrides_contract_named_in_query(tiny):
    cfg, ds = tiny
    q = "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; What is the governing law?"
    r = _split_pipe(cfg, ds).search(q, 5, document="AlphaCo")
    assert r.passages and all(x["document_id"] == "cuad/AlphaCo_License Agreement.txt" for x in r.passages)


# --- ranking-query processing ------------------------------------------------------------
def test_generic_terms_and_expansion_change_ranking_only(tiny):
    cfg, ds = tiny
    q = "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; Is there a minimum commitment in this contract?"
    base = _split_pipe(cfg, ds).retrieve(q, 5)
    tuned = _split_pipe(cfg, ds, **{"query.drop_generic_terms": True, "query.expand": True}).retrieve(q, 5)
    assert base.signals == tuned.signals  # abstention signals use the unmodified query
    idx = _split_pipe(cfg, ds, **{"query.drop_generic_terms": True, "query.expand": True}).index
    toks, weights = idx._ranking_terms("Is there a minimum commitment in this contract?",
                                       "Is there a minimum commitment in this contract?")
    assert "contract" not in toks and weights and all(0 < w < 1 for w in weights.values())
    assert "minimum" in tuned.passages[0].text.lower()


def test_expansion_rules_are_question_driven():
    from src.expansion import expansion_phrases
    assert "books" in expansion_phrases("What are the audit rights under this contract?")
    assert expansion_phrases("What is the capital city of Mongolia?") == []


def test_refined_passages_are_exact_short_and_relevant(tiny):
    cfg, ds = tiny
    p = _split_pipe(cfg, ds, **{"chunking.max_chars": 400, "chunking.overlap_chars": 0,
                                "retrieval.refine.enabled": True, "retrieval.refine.max_chars": 120})
    q = "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; Can this contract be terminated for convenience?"
    out = p.retrieve(q, 5)
    assert out.passages
    for x in out.passages:
        assert ds.documents[x.document_id][x.start_offset:x.end_offset] == x.text
    top = out.passages[0]
    assert top.end_offset - top.start_offset <= 120 and "convenience" in top.text.lower()


def test_split_signal_equals_full_without_preamble(tiny):
    cfg, ds = tiny
    out = _split_pipe(cfg, ds).retrieve("governing law", 3, document_id="cuad/AlphaCo_License Agreement.txt")
    assert out.signals["chunk_split_bm25_norm"] == out.signals["chunk_full_bm25_norm"]
    named = _split_pipe(cfg, ds).retrieve(
        "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What is the governing law?", 3)
    assert 0 < named.signals["chunk_split_bm25_norm"] < 1


# --- query refinement: debug record, original query untouched, routing unaffected -------------
def test_ranking_terms_recorded_and_query_untouched(tiny):
    cfg, ds = tiny
    q = "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; What are the audit rights under this contract?"
    p = _split_pipe(cfg, ds, **{"query.drop_generic_terms": True, "query.expand": True})
    r = p.search(q, 5)
    assert r.query == q  # the user's question is never rewritten
    exp = {t: w for t, w in r.ranking_terms.items() if w < 1.0}
    assert exp and set(exp.values()) == {0.5} and p.index.tok("books")[0] in exp  # terms + weights recorded
    assert "contract" not in r.ranking_terms  # generic template term dropped from ranking only
    plain = _split_pipe(cfg, ds).retrieve(q, 5)
    assert p.retrieve(q, 5).routed_documents == plain.routed_documents  # routing unaffected


def test_expansion_skips_function_words_when_enabled(tiny):
    cfg, ds = tiny
    q = "Can this contract be terminated for convenience?"
    on = _split_pipe(cfg, ds, **{"query.expand": True, "query.expansion_skip_function_words": True})
    off = _split_pipe(cfg, ds, **{"query.expand": True})
    any_tok = off.index.tok("any")[0]
    assert any_tok in off.index._ranking_terms(q, q)[1]
    assert any_tok not in on.index._ranking_terms(q, q)[1]


def test_generic_term_removal_keeps_negation_and_exception_words():
    from src.text import GENERIC_LEGAL_TERMS
    assert not GENERIC_LEGAL_TERMS & {"not", "no", "except", "exception", "unless", "only", "limit", "without"}
