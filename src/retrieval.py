"""Retrieval: BM25 (in-house Okapi implementation), optional dense, hybrid RRF, doc routing.

BM25 is implemented here (~60 lines) rather than via a library so that (a) the
abstention signal can use the exact query-dependent score upper bound, (b) document
routing can restrict scoring to a subset of chunks, and (c) tie handling is explicit.
Scoring (Lucene/BM25+-style non-negative idf):
    idf(t)   = ln(1 + (N - df + 0.5) / (df + 0.5))
    s(q, d)  = sum_{t in unique(q)} idf(t) * tf * (k1 + 1) / (tf + k1 * (1 - b + b * |d| / avgdl))
Normalised signal: s(q, d) / sum_{t in unique(q)} idf(t) * (k1 + 1)  in [0, 1).
Out-of-vocabulary query terms count in the denominator with df = 0, so queries about
names/terms that never occur in the corpus get a lower normalised score.
Ties: ranked by (-score, chunk_id); chunk ids follow (document_id, start_offset) order.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field, replace

import numpy as np

from .chunking import PARA_RE, SENT_RE, Chunk, chunk_corpus
from .config import index_fingerprint, resolve_path
from .expansion import EXPANSION_FUNCTION_WORDS, expansion_phrases
from .rerank import Reranker, Scorer, build_reranker
from .text import GENERIC_LEGAL_TERMS, make_tokenizer, split_query, title_from_document_id, tokenize


class BM25:
    def __init__(self, token_lists: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = float(k1), float(b)
        self.n = len(token_lists)
        self.doc_len = np.array([len(t) for t in token_lists], dtype=np.float64)
        self.avgdl = float(self.doc_len.mean()) if self.n and self.doc_len.sum() > 0 else 1.0
        postings: dict[str, tuple[list[int], list[int]]] = {}
        for i, toks in enumerate(token_lists):
            for term, tf in Counter(toks).items():
                ids, tfs = postings.setdefault(term, ([], []))
                ids.append(i)
                tfs.append(tf)
        self.postings = {t: (np.array(ids, dtype=np.int64), np.array(tfs, dtype=np.float64))
                         for t, (ids, tfs) in postings.items()}
        self.norm = self.k1 * (1.0 - self.b + self.b * self.doc_len / self.avgdl)

    def idf(self, term: str) -> float:
        df = len(self.postings[term][0]) if term in self.postings else 0
        return math.log(1.0 + (self.n - df + 0.5) / (df + 0.5))

    def scores(self, query_tokens: list[str], weights: dict[str, float] | None = None) -> np.ndarray:
        """BM25 over unique query terms; optional per-term weights (default 1.0)."""
        s = np.zeros(self.n, dtype=np.float64)
        for term in dict.fromkeys(query_tokens):  # unique, order-preserving
            if term not in self.postings:
                continue
            ids, tfs = self.postings[term]
            w = 1.0 if weights is None else float(weights.get(term, 1.0))
            s[ids] += w * self.idf(term) * tfs * (self.k1 + 1.0) / (tfs + self.norm[ids])
        return s

    def upper_bound(self, query_tokens: list[str]) -> float:
        return sum(self.idf(t) * (self.k1 + 1.0) for t in dict.fromkeys(query_tokens))


@dataclass
class Passage:
    rank: int
    document_id: str
    start_offset: int
    end_offset: int
    text: str
    score: float  # first-stage score (BM25 for method bm25); never overwritten by the reranker
    chunk_id: int
    rerank_score: float | None = None  # cross-encoder score (only when reranked)
    bm25_rank: int | None = None  # 1-based first-stage rank of this chunk (only when reranking ran)

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        for k in ("rerank_score", "bm25_rank"):  # absent when reranking is off => unchanged output
            if d[k] is None:
                del d[k]
        return d


@dataclass
class RetrievalOutput:
    passages: list[Passage]
    signals: dict[str, float]
    routed_documents: list[str] = field(default_factory=list)
    unresolved_contract: bool = False  # query names no contract and query.require_contract is on
    contract_candidates: list[str] = field(default_factory=list)  # suggestions when unresolved
    ranking_terms: dict[str, float] = field(default_factory=dict)  # debug: ranking term -> weight
    timings: dict[str, float] = field(default_factory=dict)  # rerank_seconds, n_reranked (when reranking)


class DenseEncoder:
    """Thin wrapper around sentence-transformers (optional dependency)."""

    def __init__(self, model_name: str, batch_size: int = 32):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:  # pragma: no cover - depends on optional extra
            raise ImportError("Dense retrieval needs the optional extra: uv sync --extra dense") from e
        self.model = SentenceTransformer(model_name, device="cpu")
        self.batch_size = batch_size

    def encode(self, texts: list[str]) -> np.ndarray:
        emb = self.model.encode(texts, batch_size=self.batch_size, normalize_embeddings=True,
                                show_progress_bar=len(texts) > 256, convert_to_numpy=True)
        return emb.astype(np.float32)


def dense_available() -> bool:
    try:
        import sentence_transformers  # noqa: F401
        return True
    except ImportError:
        return False


class Index:
    def __init__(self, cfg: dict, documents: dict[str, str], encoder: DenseEncoder | None = None,
                 use_cache: bool = True, reranker_scorer: Scorer | None = None):
        self.cfg = cfg
        self.documents = documents
        rcfg = cfg["retrieval"]
        self.tok = make_tokenizer(cfg["text"])
        self.chunks: list[Chunk] = chunk_corpus(documents, cfg["chunking"])
        self.doc_ids = sorted(documents)
        self.chunk_doc = np.array([self.doc_ids.index(c.document_id) for c in self.chunks], dtype=np.int64)
        index_texts = [self._index_text(c) for c in self.chunks]
        self.bm25 = BM25([self.tok(t) for t in index_texts], rcfg["bm25"]["k1"], rcfg["bm25"]["b"])
        routing = rcfg["doc_routing"]
        self.doc_bm25 = None
        if routing["enabled"]:
            self.doc_bm25 = BM25([self.tok(self._doc_text(d)) for d in self.doc_ids],
                                 rcfg["bm25"]["k1"], rcfg["bm25"]["b"])
        self.encoder = None
        self.emb = None
        if rcfg["method"] in {"dense", "hybrid"}:
            dcfg = rcfg["dense"]
            self.encoder = encoder or DenseEncoder(dcfg["model_name"], dcfg["batch_size"])
            self.emb = self._load_or_encode([dcfg["passage_prefix"] + t for t in index_texts], use_cache)
        # Second stage (lazy: the model loads on the first query that has candidates).
        self.reranker: Reranker | None = build_reranker(cfg.get("reranker"), scorer=reranker_scorer)

    # -- indexing text (search-only; never returned) --------------------------
    def _index_text(self, c: Chunk) -> str:
        if self.cfg["retrieval"]["index_doc_title"]:
            return title_from_document_id(c.document_id) + "\n" + c.text
        return c.text

    def _doc_text(self, doc_id: str) -> str:
        r = self.cfg["retrieval"]["doc_routing"]
        text = self.documents[doc_id]
        body = text if r["doc_text"] == "full" else text[: int(r["head_chars"])]
        return title_from_document_id(doc_id) + "\n" + body

    def _load_or_encode(self, texts: list[str], use_cache: bool) -> np.ndarray:
        cache = resolve_path(self.cfg["output"]["artifacts_dir"]) / "index" / index_fingerprint(self.cfg)
        path = cache / "dense_embeddings.npy"
        if use_cache and path.exists():
            emb = np.load(path)
            if emb.shape[0] == len(texts):
                return emb
        emb = self.encoder.encode(texts)
        if use_cache:
            cache.mkdir(parents=True, exist_ok=True)
            np.save(path, emb)
        return emb

    # -- retrieval -------------------------------------------------------------
    def retrieve(self, query: str, k: int, document_id: str | None = None) -> RetrievalOutput:
        """Rank passages for `query`.

        document_id: restrict retrieval to this contract (explicit user choice; skips routing).
        If query.require_contract is on (split mode), a query whose text names no contract
        ("Consider ...;" preamble missing) and has no document_id is NOT routed to an arbitrary
        best-matching contract: it returns no passages, unresolved_contract=True and the top
        routing candidates as suggestions.
        """
        rcfg, qcfg = self.cfg["retrieval"], self.cfg["query"]
        if document_id is not None and document_id not in self.documents:
            raise KeyError(f"Unknown document_id {document_id!r}")
        if not tokenize(query, lowercase=True, stopwords=True):
            # No content terms (only stopwords/punctuation/non-Latin script): no evidence possible.
            return RetrievalOutput(passages=[], signals={}, routed_documents=[])
        preamble, question = split_query(query)
        if qcfg["mode"] == "split" and preamble:
            routing_q = preamble
            chunk_q = question if qcfg["chunk_query"] == "question" else query
        else:
            routing_q, chunk_q = query, query
        signals: dict[str, float] = {}
        mask = np.ones(len(self.chunks), dtype=bool)
        routed: list[str] = []

        if document_id is not None:
            routed = [document_id]
            mask = self.chunk_doc == self.doc_ids.index(document_id)
        elif self.doc_bm25 is not None:
            rq = self.tok(routing_q)
            ds = self.doc_bm25.scores(rq)
            ub = self.doc_bm25.upper_bound(rq)
            order = sorted(range(len(self.doc_ids)), key=lambda i: (-ds[i], self.doc_ids[i]))
            if qcfg["mode"] == "split" and qcfg.get("require_contract") and not preamble:
                cands = [self.doc_ids[i] for i in order[:3] if ds[i] > 0]
                return RetrievalOutput(passages=[], signals={}, routed_documents=[],
                                       unresolved_contract=True, contract_candidates=cands)
            top = [i for i in order[: int(rcfg["doc_routing"]["top_n_docs"])] if ds[i] > 0]
            signals["doc_bm25_norm"] = float(ds[order[0]] / ub) if ub > 0 and len(order) else 0.0
            if top:
                routed = [self.doc_ids[i] for i in top]
                mask = np.isin(self.chunk_doc, top)

        cq = self.tok(chunk_q)
        bm = self.bm25.scores(cq)
        ub = self.bm25.upper_bound(cq)
        masked_bm = np.where(mask, bm, 0.0)
        signals["chunk_bm25_norm"] = float(masked_bm.max() / ub) if ub > 0 and len(bm) else 0.0
        # Evidence strength of the FULL query over the (routed) chunks, independent of which
        # query text is used for ranking. Equals chunk_bm25_norm when chunk_q == query.
        if chunk_q != query:
            fq = self.tok(query)
            fub = self.bm25.upper_bound(fq)
            fbm = np.where(mask, self.bm25.scores(fq), 0.0)
            signals["chunk_full_bm25_norm"] = float(fbm.max() / fub) if fub > 0 and len(fbm) else 0.0
        else:
            signals["chunk_full_bm25_norm"] = signals["chunk_bm25_norm"]
        # Split normalisation: preamble and question may be matched by different chunks.
        if preamble and qcfg["mode"] == "split":
            pq, qq = self.tok(preamble), self.tok(question)
            pub, qub = self.bm25.upper_bound(pq), self.bm25.upper_bound(qq)
            ps = float(np.where(mask, self.bm25.scores(pq), 0.0).max()) if len(bm) else 0.0
            qs = float(np.where(mask, self.bm25.scores(qq), 0.0).max()) if len(bm) else 0.0
            signals["chunk_split_bm25_norm"] = (ps + qs) / (pub + qub) if pub + qub > 0 else 0.0
            # Contract-identity confidence: how well the preamble matches its best chunk
            # (normally the header/recitals) of the routed contract.
            signals["preamble_bm25_norm"] = ps / pub if pub > 0 else 0.0
        else:
            signals["chunk_split_bm25_norm"] = signals["chunk_full_bm25_norm"]
            # No preamble: identity is given explicitly (document_id) or comes from routing.
            signals["preamble_bm25_norm"] = 1.0 if document_id is not None else signals.get("doc_bm25_norm", 0.0)
        # Ranking query: typed terms (optionally minus generic template words) + weighted expansion.
        rank_tokens, rank_weights = self._ranking_terms(chunk_q, question if preamble else query)
        if rank_tokens != cq or rank_weights:
            bm = self.bm25.scores(rank_tokens, rank_weights) if rank_tokens else bm
        cand = np.flatnonzero(mask)

        method = rcfg["method"]
        if method == "bm25":
            cand = cand[bm[cand] > 0]  # no lexical match => not evidence
            ranked = sorted(cand.tolist(), key=lambda i: (-bm[i], i))
            scores = {i: float(bm[i]) for i in ranked}
        else:
            qemb = self.encoder.encode([rcfg["dense"]["query_prefix"] + chunk_q])[0]
            cos = self.emb @ qemb
            signals["dense_max_cos"] = float(cos[cand].max()) if len(cand) else 0.0
            dense_rank = sorted(cand.tolist(), key=lambda i: (-cos[i], i))
            if method == "dense":
                ranked = dense_rank
                scores = {i: float(cos[i]) for i in ranked}
            else:
                h = rcfg["hybrid"]
                pool = int(h["pool"])
                bm_rank = sorted(cand[bm[cand] > 0].tolist(), key=lambda i: (-bm[i], i))[:pool]
                fused: dict[int, float] = {}
                for w, lst in ((h["bm25_weight"], bm_rank), (h["dense_weight"], dense_rank[:pool])):
                    for r, i in enumerate(lst, start=1):
                        fused[i] = fused.get(i, 0.0) + float(w) / (float(h["rrf_k"]) + r)
                ranked = sorted(fused, key=lambda i: (-fused[i], i))
                scores = fused

        # Stage 2 (optional): cross-encoder reorders the top candidates; scores/offsets untouched.
        rr_scores: dict[int, float] = {}
        bm_rank: dict[int, int] = {}
        timings: dict[str, float] = {}
        if self.reranker is not None and ranked:
            rq = (question if preamble else query) if self.cfg["reranker"]["query_text"] == "question" else query
            res = self.reranker.rerank(rq, ranked, lambda i: self.chunks[i].text)
            ranked, rr_scores, bm_rank = res.order, res.scores, res.bm25_rank
            signals["rerank_top_score"] = max(rr_scores.values())
            timings = {"rerank_seconds": res.seconds, "n_reranked": float(res.n_reranked)}

        passages = self._select(ranked, scores, k, rr_scores, bm_rank)
        if rcfg["refine"]["enabled"]:
            passages = [self._refine(p, rank_tokens, rank_weights) for p in passages]
        return RetrievalOutput(passages=passages, signals=signals, routed_documents=routed,
                               ranking_terms={t: float(rank_weights.get(t, 1.0)) for t in rank_tokens},
                               timings=timings)

    # -- ranking query & passage refinement --------------------------------------------------
    def _ranking_terms(self, chunk_q: str, question: str) -> tuple[list[str], dict[str, float]]:
        qcfg = self.cfg["query"]
        tokens = self.tok(chunk_q)
        if qcfg.get("drop_generic_terms"):
            generic = set(self.tok(" ".join(sorted(GENERIC_LEGAL_TERMS))))
            kept = [t for t in tokens if t not in generic]
            tokens = kept or tokens  # never drop the whole query
        weights: dict[str, float] = {}
        if qcfg.get("expand"):
            w = float(qcfg.get("expansion_weight", 0.5))
            typed = set(tokens)
            skip = (set(self.tok(" ".join(sorted(EXPANSION_FUNCTION_WORDS))))
                    if qcfg.get("expansion_skip_function_words") else set())
            for phrase in expansion_phrases(question):
                for t in self.tok(phrase):
                    if t in skip:
                        continue
                    if t in typed or t in weights:
                        continue
                    weights[t] = w
                    tokens.append(t)
        return tokens, weights

    def _refine(self, p: Passage, tokens: list[str], weights: dict[str, float]) -> Passage:
        """Shrink p to the contiguous sentence run (<= max_chars) with the most query-term weight.

        Units are sentences/paragraphs inside [start, end); the window score is the sum over
        DISTINCT matched terms of weight * idf. Ties: shorter window, then earlier. If no
        unit matches a query term, the passage is returned unchanged.
        """
        max_chars = int(self.cfg["retrieval"]["refine"]["max_chars"])
        text = self.documents[p.document_id]
        s0, e0 = p.start_offset, p.end_offset
        if e0 - s0 <= max_chars:
            return p
        cuts = sorted({s0, e0} | {s0 + m.end() for m in SENT_RE.finditer(text[s0:e0])}
                      | {s0 + m.end() for m in PARA_RE.finditer(text[s0:e0])})
        units = []
        for a, b in zip(cuts, cuts[1:]):
            while a < b and text[a].isspace():
                a += 1
            while b > a and text[b - 1].isspace():
                b -= 1
            if b > a:
                units.append((a, b, set(self.tok(text[a:b]))))
        qset = {t: float(weights.get(t, 1.0)) * self.bm25.idf(t) for t in dict.fromkeys(tokens)}
        best = None
        for i in range(len(units)):
            covered: set[str] = set()
            for j in range(i, len(units)):
                if units[j][1] - units[i][0] > max_chars:
                    break
                covered |= units[j][2]
                sc = sum(v for t, v in qset.items() if t in covered)
                key = (round(sc, 9), -(units[j][1] - units[i][0]), -units[i][0])
                if sc > 0 and (best is None or key > best[0]):
                    best = (key, units[i][0], units[j][1])
        if best is None:
            return p
        _, a, b = best
        return replace(p, start_offset=a, end_offset=b, text=text[a:b])

    def _select(self, ranked: list[int], scores: dict[int, float], k: int,
                rerank_scores: dict[int, float] | None = None, bm25_rank: dict[int, int] | None = None
                ) -> list[Passage]:
        """Take top-k applying the same-document overlap policy (keep | skip | trim)."""
        policy = self.cfg["retrieval"]["overlap_policy"]
        min_trim = int(self.cfg["retrieval"]["min_trimmed_chars"])
        taken: dict[str, list[tuple[int, int]]] = {}
        out: list[Passage] = []
        for i in ranked:
            if len(out) >= k:
                break
            c = self.chunks[i]
            s, e = c.start, c.end
            prev = taken.get(c.document_id, [])
            if policy != "keep" and any(ps < e and s < pe for ps, pe in prev):
                if policy == "skip":
                    continue
                s, e = _largest_uncovered(s, e, prev)
                if e - s < min_trim:
                    continue
            text = self.documents[c.document_id][s:e]
            taken.setdefault(c.document_id, []).append((s, e))
            out.append(Passage(len(out) + 1, c.document_id, s, e, text, scores[i], c.chunk_id,
                               rerank_score=(rerank_scores or {}).get(i), bm25_rank=(bm25_rank or {}).get(i)))
        return out


def _largest_uncovered(s: int, e: int, covered: list[tuple[int, int]]) -> tuple[int, int]:
    pieces = [(s, e)]
    for cs, ce in sorted(covered):
        nxt = []
        for ps, pe in pieces:
            if ce <= ps or cs >= pe:
                nxt.append((ps, pe))
                continue
            if cs > ps:
                nxt.append((ps, cs))
            if ce < pe:
                nxt.append((ce, pe))
        pieces = nxt
    if not pieces:
        return s, s
    return max(pieces, key=lambda p: (p[1] - p[0], -p[0]))
