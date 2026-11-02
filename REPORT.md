# Contract Intelligence Assistant — Evaluation Report

Scope: LegalBench-RAG-mini, CUAD only (194 queries over 29 contracts), retrieval of exact
character spans with abstention. All numbers below are copied from generated artifacts
(paths given); nothing is estimated.

## 1. Summary

A lexical (BM25) retrieval system that returns verbatim contract passages with exact source
offsets, and abstains when evidence is weak. The final configuration was chosen by a
deterministic, train-only improvement loop. Held-out **test** results (54 answerable + 7
unanswerable queries, evaluated once per configuration):

| Test metric | Baseline | **Final** |
|---|---|---|
| Precision@1 | 0.0032 | **0.1788** |
| Recall@1 | 0.0185 | **0.4328** |
| Recall@5 | 0.1278 | **0.7144** |
| F1@5 (selection objective) | 0.0138 | **0.1514** |
| Recall@64 | 0.3779 | **0.8895** |
| False abstention (answerable) | 3/54 = 5.6% | **1/54 = 1.9%** |
| Correct abstention (unanswerable) | 7/7 | 7/7 |
| Balanced abstention accuracy | 0.972 | **0.991** |
| Offset errors | 0 | 0 |

Sources: `artifacts/eval/overlap_up_test_20261102-153405/metrics.json`,
`artifacts/eval/baseline_test_20261102-153427/metrics.json`.

The main finding: CUAD queries name the contract ("Consider the … Agreement between A and B; <question>").
With the full query, party names dominate BM25 and the top passage is usually the contract
header (124/140 baseline train top-1 passages lie in the first 3,000 characters, while the right
document is found 140/140). Ranking with the question only, inside the routed contract, while
keeping the full-query abstention signal, produced most of the gain.

Precision stays low (P@5 ≈ 0.09) because returned passages (~900 chars) are much longer than
gold spans (median 317 chars) and k=5 always returns several passages.

## 2. System design

```
query ──► split "Consider <preamble>; <question>"  (query text only)
           │
           ├─ preamble ──► document-level BM25 (file-name title + first 3,000 chars) ──► top-1 contract
           │
           ├─ question ──► chunk-level BM25 over that contract's chunks ──► ranked chunks
           │                   └─ overlap policy "trim": overlapping same-doc chunks are cut to
           │                      their uncovered remainder (exact source slices)
           └─ full query ─► chunk-level BM25 over the same chunks ──► abstention signal
                                    abstain iff signal < 0.2739 (train-calibrated)
```

- **Chunking** (`src/chunking.py`): windows of ≤1,000 characters, end moved back to the best
  boundary in the last 30% (paragraph > sentence > whitespace), 300-character overlap, start
  moved to a word start. Invariant `source[start:end] == text` holds for all 2,027 final chunks
  and is re-checked on every returned passage. Source text is never altered; tokenisation
  (lowercase, stopwords, Snowball stemming) is applied only to search text.
- **BM25** (`src/retrieval.py`): implemented in-house (Okapi, k1=1.5, b=0.75, non-negative
  idf `ln(1 + (N−df+0.5)/(df+0.5))`). Reasons: exact control of the abstention normaliser,
  restriction of scoring to the routed contract, and explicit tie-breaking `(−score, chunk_id)`.
  Verified against a hand-computed score in `tests/test_retrieval.py`.
- **One pipeline** (`src/pipeline.py`) serves CLI, Streamlit app and evaluation.

Alternatives and trade-offs considered (all configurable, most tested by the loop): chunk sizes
300/500/1,000/1,500; overlap 150/300; overlap policies keep/skip/trim; stemming and stopwords;
contract title prepended to the indexing text; BM25 k1/b; document routing; question-only
ranking; four abstention signals. Dense (`all-MiniLM-L6-v2`) and hybrid RRF retrieval are
implemented and unit-tested with a stub encoder but **were not evaluated** (optional dependency
not installed); they were logged as skipped in every loop run.

## 3. LLM use

No LLM is used anywhere in the system. The task is retrieval of exact evidence spans with
offsets; an LLM is not needed to return or score spans, would add cost/latency and privacy
questions (sending contracts to a hosted model), and the brief asks not to add one without a
concrete hypothesis. A natural next hypothesis would be a cross-encoder or LLM reranker to fix
the dominant `wrong_section` failures (Section 8).

## 4. Evaluation setup

- **Data**: `benchmarks/cuad.json` (4,042 tests) → `mini()` exactly as prescribed → 194 queries
  referencing **29** contracts; only those are indexed (validated: indexed set == referenced
  set). 272 gold spans, all verified `document[start:end] == answer` using Python default
  UTF-8 text-mode reading. Files were byte-copied from the dataset and checked against its
  `SHA256SUMS` (30/30).
- **Split**: the prescribed `assign_split(query)` (SHA-256 of the stripped query, `h % 10 < 3`
  → test). Answerable: **140 train / 54 test**. Unanswerable: **28 train / 7 test**.
- **Unanswerable set** (`data/unanswerable_queries.json`, 35 queries, v1.0): authored by
  category — absent topic (13), nonexistent contract/party (11, incl. one hard negative naming
  the real Papa John's with the wrong endorser), real contract but information not stated (6),
  off-domain (5). Each query lists `absence_check_terms`; `validate-data` checks that none of them
  occurs (case-insensitive) in any indexed contract. Limitations: authored by the system builder;
  lexical absence checks cannot prove semantic absence; only 7 fall in test, so test abstention
  rates have very coarse resolution (one query = 14 points).
- **Metrics** (`src/metrics.py`), per query, top-k prefix, characters identified by
  (document, offset):
  - Precision@k = |retrieved ∩ gold| / |retrieved| (0 if nothing retrieved)
  - Recall@k = |retrieved ∩ gold| / |gold|
  - Unions of intervals are used, so duplicates are never double counted. The authors'
    pairwise-sum variant is also computed (`ref_*`); it is identical here because returned
    passages never overlap (overlap policy).
  - F1@k = per-query harmonic mean of P@k and R@k (0 if both 0), averaged. It is our selection
    objective, not a benchmark metric.
  - Aggregation: unweighted mean over queries; every aggregate carries its `n`.
  - "Retrieval" metrics use the ranked list regardless of abstention (official benchmark view);
    "with abstention" metrics treat an abstained query as an empty list.
- **Abstention metrics**: false abstention rate = abstained answerable / #answerable; correct
  abstention rate = abstained unanswerable / #unanswerable; failure-to-abstain rate =
  1 − correct abstention rate; balanced accuracy = ½·(answer rate on answerable + abstention
  rate on unanswerable).

## 5. Baseline vs final

Baseline = BM25, full query, 1,000/150 chunking, overlap policy skip, no stemming/stopwords,
abstention on `chunk_bm25_norm`. Final = `configs/final.yaml` (Section 2).

**Train** (n = 140 answerable, 28 unanswerable). Each cell is P / R / F1.

| k | Baseline | Final |
|---|---|---|
| 1 | 0.0028 / 0.0071 / 0.0040 | 0.1745 / 0.4032 / 0.2228 |
| 2 | 0.0070 / 0.0262 / 0.0110 | 0.1246 / 0.4740 / 0.1818 |
| 4 | 0.0158 / 0.1108 / 0.0264 | 0.0881 / 0.5729 / 0.1416 |
| 5 | 0.0191 / 0.1650 / 0.0328 | 0.0787 / 0.6174 / 0.1306 |
| 8 | 0.0183 / 0.2527 / 0.0330 | 0.0614 / 0.6736 / 0.1073 |
| 16 | 0.0116 / 0.2925 / 0.0219 | 0.0457 / 0.7806 / 0.0835 |
| 32 | 0.0072 / 0.3753 / 0.0140 | 0.0379 / 0.8438 / 0.0700 |
| 64 | 0.0043 / 0.4619 / 0.0084 | 0.0358 / 0.8778 / 0.0663 |
| abstention | FA 5/140, CA 28/28, BA 0.982 | FA 3/140, CA 28/28, BA 0.989 |

**Test** (n = 54 answerable, 7 unanswerable). Each cell is P / R / F1.

| k | Baseline | Final |
|---|---|---|
| 1 | 0.0032 / 0.0185 / 0.0054 | 0.1788 / 0.4328 / 0.2147 |
| 2 | 0.0086 / 0.0438 / 0.0140 | 0.1495 / 0.5616 / 0.2044 |
| 4 | 0.0096 / 0.1278 / 0.0174 | 0.1063 / 0.6708 / 0.1647 |
| 5 | 0.0075 / 0.1278 / 0.0138 | 0.0947 / 0.7144 / 0.1514 |
| 8 | 0.0087 / 0.1668 / 0.0155 | 0.0696 / 0.7363 / 0.1167 |
| 16 | 0.0093 / 0.2470 / 0.0170 | 0.0432 / 0.7967 / 0.0786 |
| 32 | 0.0069 / 0.3254 / 0.0131 | 0.0328 / 0.8668 / 0.0619 |
| 64 | 0.0044 / 0.3779 / 0.0085 | 0.0280 / 0.8895 / 0.0533 |
| abstention | FA 3/54, CA 7/7, BA 0.972 | FA 1/54, CA 7/7, BA 0.991 |

Final with abstention applied (test): P@1 0.1603, R@1 0.4283, P@5 0.0875, R@5 0.7049.
Test is slightly *better* than train for the final config; with 54 queries over few contracts
this is within sampling noise and is not evidence of anything beyond "no obvious overfitting".

## 6. Objective, guardrails, acceptance rule, thresholds

Declared in `configs/loop.yaml` before the loop ran (protocol block unchanged across all runs):

- **Primary**: `retrieval.f1@5` on train. Accept iff it improves by ≥ **0.002** (absolute) and
  all guardrails pass.
- **Guardrails** vs the currently accepted config: recall@5 drop ≤ 0.05; precision@1 drop
  ≤ 0.05; abstention balanced accuracy drop ≤ 0.05; offset errors = 0.
- Candidates are applied on top of the currently accepted config; a rejected candidate never
  replaces it (`accepted_config.yaml` is only written on acceptance).
- **Proposer**: deterministic rule — pick the first untried candidate whose tags contain the
  dominant failure category of the accepted config (diagnostics on train), else the next in
  queue order. Every iteration (accepted, rejected, skipped) is logged in `iterations.jsonl`
  with hypothesis, changes, metrics, guardrail checks, decision, reason, timestamp, git revision.
- **Test isolation**: test queries are removed from the dataset object before the loop starts;
  the negative-set file is SHA-256 hashed before/after every iteration.
- **Threshold selection** (`src/abstention.py`): per candidate, on train answerable + train
  unanswerable only. Candidate thresholds = min observed value, midpoints between consecutive
  distinct values, max + 1e-9; choose max balanced accuracy, ties → smallest threshold (fewer
  false abstentions). Rule: abstain iff no candidate passages, or signal < threshold;
  **equality answers**. Queries with no content terms (only stopwords/punctuation/non-Latin
  script) return no candidates and therefore abstain.
- **Signal** `chunk_full_bm25_norm` = best BM25 score of the *full* query over the routed
  contract's chunks ÷ Σ over unique query terms of idf(t)·(k1+1). In [0,1); not a probability.
  Out-of-vocabulary terms are included in the denominator (with df = 0), so made-up names and
  absent topics lower it. Methods with non-comparable scores have their own signals
  (`dense_max_cos`, `doc_bm25_norm`) and are calibrated separately.

## 7. Iteration history

Three loop runs, all train-only, same protocol, same frozen negative set
(SHA-256 `77d8b48ab6c6…` recorded in every run's `summary.json`). Runs took ~4 s each.

**Run 1** (`artifacts/loop/20261102-144050`, spec v1) — accepted `doc_title_in_index`:

| # | Candidate | F1@5 | R@5 | P@1 | BA | Decision |
|---|---|---|---|---|---|---|
| 0 | baseline | 0.0328 | 0.1650 | 0.0028 | 0.982 | accepted |
| 1 | question_only_chunk_query | 0.0766 | 0.4386 | 0.0965 | 0.807 | rejected: BA guardrail |
| 2 | stem_stopwords | 0.0377 | 0.2136 | 0.0087 | 0.989 | accepted |
| 3 | doc_routing | 0.0512 | 0.2748 | 0.0087 | 0.989 | accepted |
| 4 | doc_title_in_index | 0.0550 | 0.2930 | 0.0087 | 0.989 | accepted |
| 5–11 | chunk_500, overlap_trim, overlap_up, chunk_300, bm25_params, abstain_on_doc_signal, chunk_1500 | ≤0.0535 | | | | all rejected: F1 not improved |

Diagnosis after run 1 (train only): top-1 passages were contract headers; question-only ranking
more than doubled F1 but a single chunk-level signal could no longer reject queries about
nonexistent contracts (BA 0.807).

**Spec v2** added `question_only_dual_abstention` (abstain if contract match < t_doc OR question
match < t_chunk, jointly calibrated). Result: F1@5 0.0766, BA 0.904 — **rejected** (needs ≥ 0.939).
Its errors: four false abstentions on one contract whose header wording differs from the query
preamble, and four failures to abstain on "real contract, information not stated" negatives.

**Spec v3** added `question_only_fullquery_abstention`: rank with the question, keep the
full-query signal for abstention. (The v2 run's directory `run2` was later overwritten by a re-run
with spec v3; the v2 numbers above come from that run's console log, and the v3 re-run reproduces
the same `question_only_dual_abstention` result.)

**Run 3** (`artifacts/loop/run3`, spec v3; `run2` re-run is identical) — accepted `overlap_up`:

| # | Candidate | F1@5 | P@5 | R@5 | R@64 | P@1 | BA | Decision / reason |
|---|---|---|---|---|---|---|---|---|
| 0 | baseline | 0.033 | 0.019 | 0.165 | 0.462 | 0.003 | 0.982 | accepted |
| 1 | question_only_chunk_query | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.807 | rejected: BA |
| 2 | question_only_dual_abstention | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.904 | rejected: BA |
| 3 | question_only_fullquery_abstention | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.982 | **accepted** (+0.044) |
| 4 | stem_stopwords | 0.111 | 0.066 | 0.546 | 0.701 | 0.166 | 0.989 | **accepted** (+0.035) |
| – | hybrid_rrf | | | | | | | skipped: dense extra not installed |
| 5 | doc_routing | 0.051 | 0.030 | 0.275 | 0.652 | 0.009 | 0.989 | rejected (−0.060; re-enables full-query ranking) |
| 6 | doc_title_in_index | 0.109 | 0.064 | 0.539 | 0.695 | 0.164 | 0.989 | rejected (−0.003) |
| 7 | chunk_500 | 0.142 | 0.092 | 0.452 | 0.606 | 0.237 | 0.961 | rejected: recall@5 guardrail |
| 8 | overlap_trim | 0.126 | 0.075 | 0.621 | 0.878 | 0.166 | 0.989 | **accepted** (+0.015) |
| 9 | overlap_up (300) | 0.131 | 0.079 | 0.617 | 0.878 | 0.174 | 0.989 | **accepted** (+0.004) |
| 10 | chunk_300 | 0.188 | 0.136 | 0.427 | 0.670 | 0.275 | 0.925 | rejected: recall@5 + BA guardrails |
| 11 | bm25_params (k1 1.2, b 0.5) | 0.128 | 0.077 | 0.605 | 0.878 | 0.170 | 0.986 | rejected (−0.003) |
| 12 | abstain_on_doc_signal | 0.131 | 0.079 | 0.617 | 0.878 | 0.174 | 0.879 | rejected (no F1 gain) |

Notable: smaller chunks (`chunk_500`, `chunk_300`) give the highest F1 but lose >0.05 recall@5,
so the predeclared guardrail rejected them. This is the intended trade-off (do not buy precision
with large recall losses), but a different objective would choose differently.

## 8. Error analysis (train, final configuration, k = 5)

Category counts (`artifacts/error_analysis/overlap_up/summary.json`, 140 answerable): ok 24,
wrong_section 43, irrelevant_extra 37, low_rank 15, partial_span 11, chunk_boundary 7,
false_abstention 3; unanswerable: correct_abstention 28, failure_to_abstain 0.
Baseline for comparison (`artifacts/error_analysis/baseline/summary.json`): wrong_section 104,
low_rank 13, chunk_boundary 13, false_abstention 5, partial_span 4, irrelevant_extra 1, ok 0.
Twelve concrete failures (all from the final config on train; offsets are character offsets):

**Wrong section** (right contract, no gold overlap in top 5)
1. `cuad-551a572623` — BicycleTX/Crockett service agreement, *"Are there any exceptions to
   competitive restrictions?"* Gold [33572, 34034]: "save that nothing in this paragraph 13.2 shall
   prevent you from holding…". Got #1 [37817, 38817], #2 [38817, 39508]: the restrictive covenants
   themselves. Diagnosis: lexical overlap rewards the covenant, not its carve-out; "exceptions" is
   expressed as "save that".
2. `cuad-0b7b50dadf` — HPIL/GINARES cooperation agreement, *"What is the expiration date?"*
   Gold [5604, 5739]: "The term of this Agreement shall be one (1) year…". Got #1 [7739, 8739]
   (bankruptcy/insolvency boilerplate, score 2.37). Diagnosis: vocabulary gap
   (expiration ↔ term); BM25 has almost nothing to match. Motivates dense/hybrid retrieval.

**Irrelevant extra text** (gold fully in top 5, precision@5 < 0.1)
3. `cuad-e5b265c6b3` — BicycleTX, *"What is the governing law?"* Gold [53956, 54252] fully inside
   #1 [53459, 54272]; P@5 = 0.071, R@5 = 1.0. Diagnosis: correct top-1, but a 296-char answer
   inside ~4,000 returned characters.
4. `cuad-cc22d5d0ab` — HPIL, *"What is the governing law?"* Gold [16867, 17117] inside #1
   [16376, 17340]; #2 is the table of contents [1775, 2741]. P@5 = 0.059. Diagnosis: same; table
   of contents entries ("13. Notices….") match clause headings lexically.

**Low rank** (gold in top 5, but not at rank 1)
5. `cuad-5c06b5a634` — ISA/Rubicon strategic alliance, *"Exceptions to competitive restrictions?"*
   Gold [23556, 23770]; #1 [20522, 21517] and #2 [22344, 23093] are the non-compete itself.
   Diagnosis: as #1 — carve-out ranked below the restriction it modifies.
6. `cuad-92c250e51b` — Florida Chemical/Flotek supply agreement, *"Duration of any warranties?"*
   Gold [3021, 3209] ("FCC shall promptly, but in no event later than three (3) days…") reached
   only via #2 [2383, 3209]; #1 [13245, 14220] is a termination clause. Diagnosis: the annotated
   answer never says "warranty"; weak lexical signal.

**Partial span** (some gold found, recall@5 < 1, multi-span answers)
7. `cuad-e568fcd380` — ISA/Rubicon, *"How is IP ownership assigned?"* Two gold spans
   [14401, 14603], [14605, 15442]; got #1 [13158, 14127], #2 [17453, 18445] (neighbouring IP
   clauses). R@5 = 0.112. Diagnosis: many IP-heavy sections compete; the long definitional span
   is not ranked.
8. `cuad-9d8033e4f6` — Premier Biomedical IP agreement, *"Is there an exclusivity agreement?"*
   Gold [3388, 4736], [12938, 13072]; got #1 [1193, 2132] — a WHEREAS recital mentioning
   "Exclusive License". R@5 = 0.107. Diagnosis: recitals repeat key terms more densely than the
   operative clause.

**Chunk boundary** (a gold span shorter than a chunk is cut by a returned passage boundary)
9. `cuad-eb238d491d` — ISA/Rubicon, *"Exclusivity agreement?"* Gold [5690, 6079], [6537, 7080];
   got #2 [6776, 7377] (start produced by overlap trimming) covering only the tail of the second
   span. R@5 = 0.592. Diagnosis: the trim policy keeps the uncovered remainder, which can begin
   mid-clause.
10. `cuad-dd123231af` — ISA/Rubicon, *"What licenses are granted?"* Same gold region; R@5 = 0.581.
    Diagnosis: licence grant split across chunks; the most relevant chunk ranks below
    IP-reservation clauses.

**False abstention** (answerable, signal < 0.2739)
11. `cuad-2f7d42bc6c` — BicycleTX, *"Any right of first refusal / first offer / first negotiation?"*
    Signal 0.245. Gold [6235, 6531], [6533, 7937] describe a share-option arrangement. Diagnosis:
    the annotated answer shares almost no vocabulary with the question; low evidence is
    "correctly" low, so the threshold rejects it.
12. `cuad-7646cba011` — BicycleTX, *"How is IP ownership assigned?"* Signal 0.248, yet #1
    [44251, 45248] covered 79% of the gold span [44840, 45359]. Diagnosis: a good answer thrown
    away — the long contract and the generic question give a low normalised score. This is the
    cost side of the threshold.

Machine-readable: `artifacts/error_analysis/overlap_up/failures.jsonl` (116 records) and
`artifacts/error_analysis/baseline/failures.jsonl` (140 records).

**Held-out test behaviour** (not used for any change): final R@5 0.714 vs 0.617 on train,
1 false abstention in 54, all 7 unanswerable test queries rejected. The test set was not
analysed per query to avoid informing further changes.

## 9. Limitations, risks, next steps

- **Query format dependence.** Routing relies on the CUAD "Consider …;" preamble. A question
  without it (e.g. "What restrictions apply to sublicensing?") is routed to whichever single
  contract matches best, which is often wrong. Real users would need a contract selector or
  multi-document retrieval (`top_n_docs` > 1).
- **Single-contract routing.** If routing picks the wrong contract, recall is 0 for that query.
  It was correct for 140/140 train queries, but parties were named explicitly.
- **Low precision.** About 900-char passages for about 300-char answers. Sentence-level refinement inside the
  top chunks, or smaller chunks with a recall-aware objective, are the obvious next experiments.
- **Lexical retrieval.** Vocabulary gaps (expiration ↔ term, exceptions ↔ "save that") cause
  most `wrong_section` failures. Dense/hybrid retrieval is implemented but unevaluated; a
  cross-encoder reranker is the next hypothesis.
- **Abstention evidence is weak in two ways.** (a) Only 7 test negatives — 95% intervals are
  very wide. (b) The negative set was hand-authored by the system's developers and many
  negatives contain out-of-vocabulary words, which the signal is designed to catch;
  realistic negatives (plausible question about a real contract where the answer is absent)
  are harder, as the v2 experiment showed.
- **Small, homogeneous benchmark.** 29 contracts, 194 queries; differences of a few hundredths
  in train metrics (e.g. +0.004 for `overlap_up`) are not statistically meaningful.
- **Not legal advice.** The system returns excerpts; it does not interpret them. Before real
  legal use: lawyer-validated evaluation on the target contract population, calibration of the
  abstention rule on realistic negatives, document-level access control, and audit logging.

## 10. Test-set runs and inspections

Recorded automatically in `artifacts/test_runs.jsonl` (the CLI refuses the test split without
`--final-test`). **Three** test evaluations were run:

| # | Time (IST) | Config | Purpose |
|---|---|---|---|
| 1 | 2026-11-02 14:42 | `provisional` (baseline-equivalent BM25 config, before any final selection) | early runbook check during setup |
| 2 | 2026-11-02 15:34 | `overlap_up` (final) | final evaluation |
| 3 | 2026-11-02 15:34 | `baseline` | baseline comparison for this report |

Run #1 happened before the final configuration existed. No configuration, candidate, or
threshold was changed on the basis of its results: all later changes (spec v2, v3) were
motivated by train diagnostics only, as documented in Section 7 and in the `configs/loop.yaml`
change log. The improvement loop code never loads test queries. Runs #2 and #3 were made after
the final configuration was committed (`b4dbca3`), and no changes followed them.

Integrity note: the unanswerable set was committed (`20e9cf4`, 14:44 IST) about four minutes
after loop run 1 started (14:40 IST). The file was authored before any loop run and its SHA-256
(`77d8b48ab6c6…`) is identical in all three loop runs' `summary.json` and in the committed file, so
its content did not change during or after experimentation.
