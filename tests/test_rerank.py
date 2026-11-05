"""Second-stage reranker (src/rerank.py) with mocked scorers: no model download in ordinary CI."""

from __future__ import annotations

import math
import sys
import types

import pytest
import yaml

from src import cli
from src.config import apply_overrides, config_fingerprint, load_config
from src.evaluation import evaluate, write_results
from src.pipeline import Pipeline, PipelineError
from src.rerank import CrossEncoderScorer, Reranker, RerankError, build_reranker

Q_INS = "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; What are the insurance requirements?"
Q_LAW = "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What is the governing law for this contract?"


class KeywordScorer:
    """Deterministic mock: score = occurrences of `word` in the passage; records every call."""

    def __init__(self, word: str = "insurance"):
        self.word, self.calls, self.batch_sizes = word, [], []

    def score(self, query, texts, batch_size):
        self.calls.append((query, list(texts)))
        self.batch_sizes.append(batch_size)
        return [float(t.lower().count(self.word)) for t in texts]


class ConstantScorer(KeywordScorer):
    def score(self, query, texts, batch_size):
        super().score(query, texts, batch_size)
        return [0.5] * len(texts)


class ReverseScorer(KeywordScorer):
    """Scores strictly decreasing with input position reversed => reverses the BM25 order."""

    def score(self, query, texts, batch_size):
        super().score(query, texts, batch_size)
        return [float(i) for i in range(len(texts))]


class FailingScorer:
    def __init__(self, exc: Exception):
        self.exc = exc

    def score(self, query, texts, batch_size):
        raise self.exc


class BadScorer:
    def __init__(self, result):
        self.result = result

    def score(self, query, texts, batch_size):
        return self.result(texts)


class MustNotBeCalled:
    def score(self, query, texts, batch_size):
        raise AssertionError("scorer called on an empty candidate list")


def _on(cfg, **kw):
    over = {"reranker.enabled": True, **{f"reranker.{k}": v for k, v in kw.items()}}
    return apply_overrides(cfg, over)


def _spans(passages):
    return [(p.document_id, p.start_offset, p.end_offset) for p in passages]


# -- configuration ---------------------------------------------------------------------------

def test_disabled_by_default_and_in_frozen_configs():
    from src.config import DEFAULTS
    assert DEFAULTS["reranker"]["enabled"] is False
    for path in ("configs/final.yaml", "configs/candidate_v4.yaml"):
        cfg = load_config(path)
        assert cfg["reranker"]["enabled"] is False
        assert build_reranker(cfg["reranker"]) is None


def test_disabled_reranker_does_not_change_fingerprint(tiny):
    cfg, _ = tiny
    base = config_fingerprint(cfg)
    assert config_fingerprint(apply_overrides(cfg, {"reranker.candidate_k": 7})) == base
    assert config_fingerprint(_on(cfg)) != base


def test_config_validation():
    with pytest.raises(ValueError):
        load_config(None, {"abstention.signal": "rerank_top_score"})  # needs reranker.enabled
    with pytest.raises(ValueError):
        load_config(None, {"reranker.enabled": True, "reranker.candidate_k": 0})
    with pytest.raises(ValueError):
        load_config(None, {"reranker.enabled": True, "reranker.backend": "llm"})
    with pytest.raises(ValueError):
        load_config(None, {"reranker.enabled": True, "reranker.query_text": "preamble"})
    cfg = load_config("configs/experiments/exp6_cross_encoder.yaml")
    assert cfg["reranker"]["enabled"] and cfg["reranker"]["device"] == "cpu"
    v4 = load_config("configs/candidate_v4.yaml")
    for section in ("data", "chunking", "text", "query", "retrieval", "evaluation"):
        assert cfg[section] == v4[section]  # experiment = candidate_v4 + reranker only
    assert cfg["abstention"]["signal"] == v4["abstention"]["signal"]


# -- Reranker unit behaviour --------------------------------------------------------------

def test_reorders_by_score_and_keeps_bm25_tail():
    r = Reranker(KeywordScorer("x"), candidate_k=3, batch_size=2)
    texts = {10: "a", 11: "x", 12: "xx", 13: "xxx", 14: "xxxx"}
    res = r.rerank("q", [10, 11, 12, 13, 14], texts.__getitem__)
    assert res.order == [12, 11, 10, 13, 14]  # head reranked, tail (13, 14) untouched despite higher counts
    assert res.scores == {10: 0.0, 11: 1.0, 12: 2.0}
    assert res.bm25_rank == {10: 1, 11: 2, 12: 3, 13: 4, 14: 5}
    assert res.n_reranked == 3


def test_equal_scores_keep_bm25_order():
    res = Reranker(ConstantScorer(), candidate_k=10).rerank("q", [5, 2, 9, 1], lambda i: "t")
    assert res.order == [5, 2, 9, 1]


def test_empty_candidates_never_call_or_load_model():
    res = Reranker(MustNotBeCalled()).rerank("q", [], lambda i: "t")
    assert res.order == [] and res.scores == {} and res.n_reranked == 0


def test_fewer_candidates_than_candidate_k():
    s = KeywordScorer()
    res = Reranker(s, candidate_k=50).rerank("q", [3, 1], lambda i: f"t{i}")
    assert sorted(res.order) == [1, 3] and res.n_reranked == 2
    assert len(s.calls[0][1]) == 2


def test_duplicate_candidates_scored_once():
    s = KeywordScorer()
    res = Reranker(s, candidate_k=10).rerank("q", [4, 2, 4, 7, 2], lambda i: f"t{i}")
    assert sorted(res.order) == [2, 4, 7] and len(res.order) == 3
    assert s.calls[0][1] == ["t4", "t2", "t7"]


@pytest.mark.parametrize("bad", [lambda t: [1.0] * (len(t) - 1), lambda t: [math.nan] * len(t),
                                 lambda t: ["high"] * len(t)])
def test_bad_inference_output_raises(bad):
    with pytest.raises(RerankError):
        Reranker(BadScorer(bad)).rerank("q", [1, 2], lambda i: "t")


def test_invalid_reranker_sizes():
    with pytest.raises(ValueError):
        Reranker(KeywordScorer(), candidate_k=0)
    with pytest.raises(ValueError):
        Reranker(KeywordScorer(), batch_size=0)


# -- CrossEncoderScorer with a fake sentence_transformers module ----------------------------

def _fake_st(monkeypatch, *, fail_load=False, fail_predict=False):
    created = []

    class FakeCE:
        def __init__(self, name, **kw):
            if fail_load:
                raise OSError("model not found")
            created.append((name, kw))
            self.model = types.SimpleNamespace(parameters=lambda: [types.SimpleNamespace(numel=lambda: 7)])
            self.predict_calls = []

        def predict(self, pairs, batch_size, show_progress_bar, convert_to_numpy):
            if fail_predict:
                raise RuntimeError("boom")
            import numpy as np
            self.predict_calls.append(batch_size)
            return np.array([float(len(p)) for _, p in pairs], dtype=np.float32)

    monkeypatch.setitem(sys.modules, "sentence_transformers", types.SimpleNamespace(CrossEncoder=FakeCE))
    return created


def test_model_loads_lazily_on_cpu_with_batch_size(monkeypatch, tiny):
    cfg, ds = tiny
    created = _fake_st(monkeypatch)
    pipe = Pipeline(_on(cfg, batch_size=3, device="cpu"), ds.documents)
    assert created == []  # building the index does not load the model
    out = pipe.retrieve(Q_INS, 5)
    assert len(created) == 1
    name, kw = created[0]
    assert name == "cross-encoder/ms-marco-MiniLM-L-6-v2" and kw["device"] == "cpu"
    assert kw["max_length"] == 512 and kw["local_files_only"] is False
    scorer = pipe.index.reranker.scorer
    assert scorer._model.predict_calls == [3] and scorer.load_seconds is not None and scorer.n_parameters == 7
    assert all(p.rerank_score is not None for p in out.passages)
    pipe.retrieve(Q_LAW, 5)
    assert len(created) == 1  # loaded once


def test_model_loading_failure_is_reported(monkeypatch, tiny):
    cfg, ds = tiny
    _fake_st(monkeypatch, fail_load=True)
    with pytest.raises(RerankError, match="Could not load cross-encoder"):
        CrossEncoderScorer("nope/nope", local_files_only=True).score("q", ["t"], 1)
    pipe = Pipeline(_on(cfg), ds.documents)
    with pytest.raises(PipelineError, match="Reranking failed"):
        pipe.search(Q_INS, 3)


def test_missing_optional_dependency_is_reported(monkeypatch):
    monkeypatch.setitem(sys.modules, "sentence_transformers", None)  # import raises ImportError
    with pytest.raises(RerankError, match="uv sync --extra dense"):
        CrossEncoderScorer("x").score("q", ["t"], 1)


def test_inference_failure_is_reported(monkeypatch, tiny):
    cfg, ds = tiny
    _fake_st(monkeypatch, fail_predict=True)
    with pytest.raises(RerankError, match="inference failed"):
        CrossEncoderScorer("x").score("q", ["t"], 1)
    with pytest.raises(PipelineError):
        Pipeline(_on(cfg), ds.documents).retrieve(Q_INS, 3)
    with pytest.raises(PipelineError):  # an injected scorer failing mid-query is not swallowed either
        Pipeline(_on(cfg), ds.documents, reranker_scorer=FailingScorer(RerankError("x"))).retrieve(Q_INS, 3)


# -- integration with retrieval --------------------------------------------------------------

def test_disabled_output_identical_to_bm25(tiny):
    cfg, ds = tiny
    a = Pipeline(cfg, ds.documents).retrieve(Q_INS, 10)
    b = Pipeline(apply_overrides(cfg, {"reranker.enabled": False}), ds.documents,
                 reranker_scorer=MustNotBeCalled()).retrieve(Q_INS, 10)
    assert [p.to_dict() for p in a.passages] == [p.to_dict() for p in b.passages]
    assert a.signals == b.signals and b.timings == {}
    assert "rerank_score" not in a.passages[0].to_dict() and "bm25_rank" not in a.passages[0].to_dict()


def test_constant_scores_reproduce_bm25_order(tiny):
    cfg, ds = tiny
    a = Pipeline(cfg, ds.documents).retrieve(Q_LAW, 10)
    b = Pipeline(_on(cfg), ds.documents, reranker_scorer=ConstantScorer()).retrieve(Q_LAW, 10)
    assert _spans(a.passages) == _spans(b.passages)
    assert [p.score for p in a.passages] == [p.score for p in b.passages]


def test_reranking_preserves_ids_offsets_text_and_bm25_scores(tiny):
    cfg, ds = tiny
    cfg = apply_overrides(cfg, {"retrieval.overlap_policy": "keep"})  # passage == chunk, so ids compare 1:1
    base = Pipeline(cfg, ds.documents).retrieve(Q_INS, 16)
    pipe = Pipeline(_on(cfg), ds.documents, reranker_scorer=ReverseScorer())
    out = pipe.retrieve(Q_INS, 16)
    bm25_by_chunk = {p.chunk_id: p for p in base.passages}
    assert sorted(bm25_by_chunk) == sorted(p.chunk_id for p in out.passages)  # same candidates
    assert [p.chunk_id for p in out.passages] == [p.chunk_id for p in base.passages][::-1]  # order reversed
    assert [p.rank for p in out.passages] == list(range(1, len(out.passages) + 1))
    for p in out.passages:
        ref = bm25_by_chunk[p.chunk_id]
        assert (p.document_id, p.start_offset, p.end_offset, p.text) == \
               (ref.document_id, ref.start_offset, ref.end_offset, ref.text)
        assert p.score == ref.score  # BM25 score preserved
        assert p.bm25_rank == ref.rank  # chunk-level BM25 rank recorded
        assert p.rerank_score is not None
        assert ds.documents[p.document_id][p.start_offset:p.end_offset] == p.text
    assert out.signals["rerank_top_score"] == max(p.rerank_score for p in out.passages)
    assert out.timings["n_reranked"] == len(out.passages)


def test_reranker_moves_relevant_chunk_to_top(tiny):
    cfg, ds = tiny
    q = "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; What does the supplier maintain?"
    out = Pipeline(_on(cfg), ds.documents, reranker_scorer=KeywordScorer("insurance")).retrieve(q, 5)
    assert "insurance" in out.passages[0].text.lower()


def test_reranker_sees_question_only_and_routed_chunks(tiny):
    cfg, ds = tiny
    cfg = apply_overrides(cfg, {"query.mode": "split", "query.chunk_query": "question",
                                "retrieval.doc_routing.enabled": True})
    s = KeywordScorer()
    out = Pipeline(_on(cfg), ds.documents, reranker_scorer=s).retrieve(Q_INS, 5)
    assert s.calls[0][0] == "What are the insurance requirements?"
    assert {p.document_id for p in out.passages} == {"cuad/BetaInc_Supply Agreement.txt"}
    s_full = KeywordScorer()
    Pipeline(_on(cfg, query_text="full"), ds.documents, reranker_scorer=s_full).retrieve(Q_INS, 5)
    assert s_full.calls[0][0] == Q_INS


def test_document_filter_respected(tiny):
    cfg, ds = tiny
    doc = "cuad/AlphaCo_License Agreement.txt"
    s = KeywordScorer("insurance")
    r = Pipeline(_on(cfg), ds.documents, reranker_scorer=s).search(Q_INS, 5, document="AlphaCo")
    assert r.document_filter == doc
    assert all(p["document_id"] == doc for p in r.passages)
    assert all(t in ds.documents[doc] for _, texts in s.calls for t in texts)  # only filtered chunks scored


def test_no_candidates_skips_model(tiny):
    cfg, ds = tiny
    r = Pipeline(_on(cfg), ds.documents, reranker_scorer=MustNotBeCalled()).search("quintessor zorblax", 5)
    assert r.abstained and r.abstention_reason == "no_candidates" and r.passages == []


def test_abstention_unchanged_by_reranking(tiny):
    cfg, ds = tiny
    cfg = apply_overrides(cfg, {"query.mode": "split", "query.chunk_query": "question",
                                "retrieval.doc_routing.enabled": True,
                                "abstention.signal": "chunk_full_bm25_norm", "abstention.threshold": 0.2})
    a = Pipeline(cfg, ds.documents)
    b = Pipeline(_on(cfg), ds.documents, reranker_scorer=ReverseScorer())
    for q in [Q_INS, Q_LAW, "What does the agreement say about quintessor obligations?"]:
        ra, rb = a.search(q, 5), b.search(q, 5)
        assert (ra.abstained, ra.abstention_reason, ra.signal_value) == (rb.abstained, rb.abstention_reason,
                                                                          rb.signal_value)
        oa, ob = a.retrieve(q), b.retrieve(q)
        assert {k: v for k, v in ob.signals.items() if k != "rerank_top_score"} == oa.signals


def test_rerank_top_score_abstention_signal(tiny):
    cfg, ds = tiny
    c = _on(cfg)
    c = apply_overrides(c, {"abstention.signal": "rerank_top_score", "abstention.threshold": 1.0})
    pipe = Pipeline(c, ds.documents, reranker_scorer=KeywordScorer("insurance"))
    assert not pipe.search(Q_INS, 3).abstained  # top score 1.0 >= 1.0 (equality answers)
    assert pipe.search(Q_LAW, 3).abstained  # no passage mentions insurance => 0.0 < 1.0


# -- evaluation / CLI ------------------------------------------------------------------------

def test_evaluation_records_rerank_scores_and_operational_metrics(tiny, tmp_path):
    cfg, ds = tiny
    c = _on(cfg)
    res = evaluate(c, ds, "train", pipeline=Pipeline(c, ds.documents, reranker_scorer=KeywordScorer()))
    assert res["offset_errors"] == 0
    op = res["operational"]
    assert op["n_reranked_queries"] > 0 and op["mean_rerank_seconds"] is not None and op["peak_rss_mib"] > 0
    answered = [r for r in res["per_query"] if r["retrieved"]]
    assert answered and all("rerank_score" in x and "bm25_rank" in x for r in answered for x in r["retrieved"])
    out = write_results(res, tmp_path / "ev")
    assert (out / "metrics.json").exists()
    base = evaluate(cfg, ds, "train")
    assert base["operational"]["n_reranked_queries"] == 0
    assert all("rerank_score" not in x for r in base["per_query"] for x in r["retrieved"])


def test_compare_cli(tiny, tmp_path, capsys):
    cfg, ds = tiny
    a = write_results(evaluate(cfg, ds, "train"), tmp_path / "a")
    c = _on(cfg)
    b = write_results(evaluate(c, ds, "train", pipeline=Pipeline(c, ds.documents, reranker_scorer=ReverseScorer())),
                      tmp_path / "b")
    qid = next(r["qid"] for r in evaluate(cfg, ds, "train")["per_query"] if r["answerable"])
    rc = cli.main(["compare", str(a), str(b), "--qids", qid, "--out", str(tmp_path / "cmp.json")])
    text = capsys.readouterr().out
    assert rc == 0 and "recall@10 (top-10 recompute)" in text and "recompute check (k=5) | ok | ok" in text
    assert qid in text and (tmp_path / "cmp.json").exists()


def test_cli_search_shows_rerank_score(tiny, tmp_path, capsys, monkeypatch):
    cfg, _ = tiny
    _fake_st(monkeypatch)
    p = tmp_path / "cfg.yaml"
    p.write_text(yaml.safe_dump(_on(cfg)), encoding="utf-8")
    rc = cli.main(["search", "--query", Q_INS, "--top-k", "2", "--config", str(p)])
    assert rc == 0 and "rerank=" in capsys.readouterr().out


# -- optional: the real model (needs the `dense` extra and a cached download) ------------------

def _real_model_available() -> bool:
    try:
        CrossEncoderScorer("cross-encoder/ms-marco-MiniLM-L-6-v2", local_files_only=True)._load()
        return True
    except RerankError:
        return False


@pytest.mark.dense
def test_real_cross_encoder_smoke(tiny):
    if not _real_model_available():
        pytest.skip("cross-encoder not installed/cached (uv sync --extra dense; download once)")
    cfg, ds = tiny
    c = _on(cfg, local_files_only=True)
    out = Pipeline(c, ds.documents).retrieve(Q_INS, 5)
    assert out.passages and all(isinstance(p.rerank_score, float) for p in out.passages)
    scores = [p.rerank_score for p in out.passages]
    assert scores == sorted(scores, reverse=True)
    assert all(ds.documents[p.document_id][p.start_offset:p.end_offset] == p.text for p in out.passages)
