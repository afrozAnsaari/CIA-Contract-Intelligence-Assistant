# Contract Intelligence Assistant — Technical Report

**Evidence conventions.** Every number in this report comes from a file in the repository; the
path is given next to each table. Numbers checked again while writing this report are marked
*(re-checked)*. These checks compared saved artifacts with each other and re-ran cheap,
train-only computations; no test-split evaluation was re-run. Statements that rest only on the
developer's session record, with no surviving artifact, are marked *(session record only)*.

## 1. Executive summary

- **Objective.** Given a question about a commercial contract, return ranked verbatim passages
  with exact character offsets that contain the evidence, or abstain when the indexed contracts
  don't support an answer.
- **Approach.** Lexical BM25 retrieval over offset-preserving chunks of the 29 CUAD contracts
  referenced by LegalBench-RAG-mini. In the final configuration:
  - the query's contract preamble ("Consider the … Agreement between A and B;") selects one
    contract;
  - the question part ranks that contract's chunks;
  - a normalised BM25 score of the full query decides abstention, with a threshold tuned on
    training data.

  No LLM, embedding model or learned reranker is used in the evaluated configurations.
- **Evaluation.**
  - Character-level precision and recall at k ∈ {1, 2, 4, 5, 8, 16, 32, 64} on the prescribed
    split (140 train / 54 test answerable queries).
  - Abstention on those queries and on 35 hand-authored unanswerable queries (28 train / 7 test).
  - Configuration chosen by a train-only improvement loop.
- **Held-out test results** for the final configuration, from saved artifacts *(re-checked)*:
  - P@1 = 0.1788, R@1 = 0.4328
  - P@5 = 0.0947, R@5 = 0.7144, F1@5 = 0.1514
  - R@64 = 0.8895
  - false abstention 1/54; correct abstention 7/7

  For the baseline: R@5 = 0.1278 and F1@5 = 0.0138.
- **Most important limitations.**
  - Precision is low. Returned passages average about 785 characters (train, top 5), while gold
    spans have a median of about 317, so most retrieved text is not gold evidence.
  - Abstention is evaluated on only 7 test negatives.
  - The evaluation protocol has documented deviations (§9): the negative set was committed
    after the first loop run started, and the test split was evaluated three times.

## 2. Problem formulation and scope

- **Input:** a natural-language question.
- **Output:** either a ranked list of passages (`document_id`, `start_offset`, `end_offset`,
  `text`, `score`, `rank`), or an explicit abstention with no passages.
- **Corpus:** only the CUAD part of LegalBench-RAG is in scope, reduced to the LegalBench-RAG-mini
  selection. Only the contracts referenced by the selected queries are indexed, so findings apply
  to these 29 SEC-filed commercial contracts and these question types, not to legal documents in
  general.
- **Answerable query:** a benchmark query with annotated gold character spans. Every such query
  has at least one gold span; the 194 queries have 272 spans in total.
- **Unanswerable query:** a hand-authored query whose answer is not stated in any indexed
  contract (§4). The correct behaviour is to abstain.

## 3. Dataset construction and split

| Step | Implementation | Verified result *(re-checked with `validate-data` logic)* |
|---|---|---|
| Load benchmark | `benchmarks/cuad.json` (`src/data.py: load_mini_tests`) | 4,042 tests; SHA-256 `8e0405b15fb8…` matches the dataset's `SHA256SUMS` |
| Mini selection | `mini(tests, n=194)`: sort by `random.seed(t["snippets"][0]["file_path"]); random.random()`, take the first 194 (`src/data.py: mini`, same as the prescribed function) | 194 queries |
| Referenced contracts | the set of `snippets[*].file_path` of the selected queries (`referenced_documents`) | 29 contracts; indexed set == referenced set |
| Split | `assign_split(query)`: `h = int(sha256(query.strip().encode("utf-8")).hexdigest(), 16)`; `test if h % 10 < 3 else train` | 140 train / 54 test answerable; matches the prescribed function for all 229 queries |
| Gold validation | `document[start:end] == answer` on the decoded source (`validate_dataset`) | 272/272 spans match; no query has overlapping gold spans |

- **Split input.** The only preprocessing before hashing is `str.strip()`, which is part of the
  prescribed rule. Unanswerable queries use the same function.
- **Offset convention.** Offsets are Python string indices into
  `open(path, encoding="utf-8").read()` (default text mode, so universal newline translation
  applies). Source text is never normalised. Tokenisation, lowercasing, stemming and stopword
  removal apply only to search-side copies.
- **Data preparation.** `prepare-data` byte-copies `cuad.json` and the 29 referenced contracts
  into `data/raw/` and checks each against `SHA256SUMS` (30/30). It writes
  `data/processed/manifest.json` (SHA-256 `204a4d7efb3a…`).
- **What the split doesn't guarantee.** The hash split is deterministic, but it doesn't make
  leakage impossible. Many train and test queries ask different questions about the **same
  contract**: all 29 contracts are shared between the splits, and question templates repeat
  across contracts. So test results measure generalisation to new (contract, question) pairs
  within the same 29 contracts, not to unseen contracts.

## 4. Unanswerable-query set

[`data/unanswerable_queries.json`](data/unanswerable_queries.json), version 1.0, SHA-256
`77d8b48ab6c6…`.

| Category | Count | What it tests | Example |
|---|---|---|---|
| `absent_topic` | 13 | topic not covered by any indexed contract | "What cryptocurrency or blockchain token is used to settle payments under this contract?" |
| `nonexistent_contract` | 11 | names a contract/party that isn't indexed (one hard case uses the real Papa John's with the wrong endorser) | "Consider the Lease Agreement between Quillon Properties LLC and Marrowgate Foods Inc.; What is the monthly rent…?" |
| `unspecified_info` | 6 | a **real indexed contract**, asking for information it doesn't state | "Consider the Non-Competition Agreement of Western Copper; What is the current copper price on the London Metal Exchange?" |
| `off_domain` | 5 | general-knowledge questions | "Who won the FIFA World Cup in 2018?" |
| **Total** | **35** | split with `assign_split`: **28 train / 7 test** *(re-checked)* | |

**Construction and checks.**
- The set was hand-authored by category, with a written rationale for each query.
- Each query lists `absence_check_terms`. `validate-data` checks, case-insensitively, that none
  of them occurs in any indexed contract; all 35 pass.
- The IDs and query texts are unique, and none duplicates a benchmark query.

**Freezing.**
- The file was first committed in `20e9cf4` (2026-11-02 14:44:58 IST).
- Its content never changed afterwards: the same SHA-256 is recorded in all three loop runs'
  `summary.json` and matches the committed file.
- Commit timing relative to the first loop run is discussed in §9.

**Limitations.**
- **Lexical checks.** The absence checks are lexical. They can't prove semantic absence:
  paraphrases or synonyms of an absent term could still occur.
- **A borderline query.** `unans-011` ("Which party is responsible for sponsoring immigration
  petitions for foreign workers?") is unanswerable as written, but two UK service agreements
  contain a nearby clause about the employee's "right to work in the United Kingdom". It is a
  harder negative than intended and was left unchanged because the set is frozen.
- **Few realistic negatives.** Only the 6 `unspecified_info` queries, plus the Papa John's hard
  case, are realistic "plausible question about a real contract, answer absent" negatives. The
  `nonexistent_contract` and `absent_topic` queries contain words that never occur in the
  corpus, which the BM25 evidence signal is designed to penalise. They are easier than realistic
  negatives.
- **Small test portion.** Only **7** negatives fall in test (4 without a contract preamble, 3
  with one). The test abstention rates therefore have very low resolution; see §11.
- **Authorship.** The set was written by the developer with an AI assistant, the same people who
  built the system. It wasn't independently reviewed.

## 5. System architecture

```
query
 ├─ src/text.py split_query: "Consider <preamble>; <question>"  (query text only)
 ├─ contract selection (src/retrieval.py Index.retrieve)
 │    explicit document_id ─────────────────────────────► that contract
 │    preamble present ─► BM25 over [file-name title + first 3,000 chars] of each contract ─► top-1
 │    no preamble ─► require_contract=true: abstain "contract_not_identified" + 3 suggestions
 ├─ ranking: BM25 of the QUESTION over the selected contract's chunks; ties by (−score, chunk_id)
 ├─ overlap policy "trim": a chunk overlapping an already-selected passage of the same contract
 │    is cut to its largest uncovered piece (dropped if < 50 chars); still an exact source slice
 ├─ abstention signal: BM25 of the FULL query over the same chunks (chunk_full_bm25_norm)
 │    abstain iff no candidates, or signal < threshold (0.2739); equality answers
 └─ output: passages with exact offsets (re-validated in src/pipeline.py), or abstention
```

**Loading.** Contracts are plain-text CUAD files read without modification (`src/data.py`).

**Chunking** (`src/chunking.py`).
- Windows of at most `max_chars` characters (1,000 in the final configuration).
- Each window's end is moved back to the best boundary within its last 30%: paragraph break,
  then sentence end, then whitespace.
- The next window starts `overlap_chars` (300) before the previous end, moved forward to the next
  word start.
- The invariant `source[start:end] == text` is tested and checked on every returned passage.
- The final configuration has 2,027 chunks (mean 889 characters); the baseline has 1,617.

**BM25** (`src/retrieval.py: BM25`).
- In-house Okapi BM25 with k1 = 1.5 and b = 0.75, using the non-negative idf
  `ln(1 + (N − df + 0.5)/(df + 0.5))` and summing over unique query terms.
- It is written in-house so that scoring can be restricted to one contract, the abstention
  normaliser is exact, and tie-breaking is explicit.
- It is checked against a hand-computed score in `tests/test_retrieval.py`.

**Contract routing and query representation.**
- The preamble names the agreement and its parties. That is the best signal for *which*
  contract, but it is a poor signal for *where* in the contract the answer is.
- With the full query, party names dominate chunk scores. In the baseline, 124 of 140 train
  top-1 passages came from the first 3,000 characters of the contract, which is the party/recital
  header (`artifacts/loop/20261102-144050/iter00_baseline/per_query.jsonl`, *re-checked*).
- So the preamble is used only for routing, and the question alone ranks chunks. With the final
  configuration, routing picks a gold contract for **140/140** train queries *(re-checked from
  `artifacts/loop/run3/iter09_overlap_up/per_query.jsonl`)*.

**Abstention** (`src/abstention.py`, §6).
- The signal is computed from the full query even though ranking uses the question. Made-up
  party names and absent topics consist of words that don't occur in the corpus, and those lower
  the normalised score.
- Abstention and ranking are separate design decisions. §8 shows why.

**Evaluation and loop.** `src/evaluation.py`, `src/metrics.py`, `src/diagnostics.py`,
`src/improvement_loop.py` (§6, §8).

**Models.**
- No LLM is used, and no model was trained or fine-tuned.
- A dense retriever (sentence-transformers `all-MiniLM-L6-v2`) and hybrid RRF are implemented
  behind an optional dependency and tested only with a stub encoder. They were **never
  evaluated**: the dependency wasn't installed, so the loop logged them as skipped.

## 6. Output format and evaluation definitions

**Passage fields** (`src/retrieval.py: Passage`; serialised by `Pipeline.search`):

| Field | Meaning |
|---|---|
| `rank` | 1-based position after overlap handling |
| `document_id` | benchmark file path, e.g. `cuad/<file>.txt` |
| `start_offset`, `end_offset` | half-open `[start, end)` Python string indices into the source text |
| `text` | `source[start_offset:end_offset]`, exactly |
| `score` | BM25 score of the ranking query (dense/hybrid would use cosine or RRF) |
| `chunk_id` | internal chunk identifier |

A search result also carries `abstained`, `abstention_reason`, `signal`, `signal_value`,
`threshold`, `document_filter` and `contract_candidates`.

**Retrieval metrics** (`src/metrics.py`). For a query with gold character set G, and R the union
of characters covered by the first k returned passages (characters identified by
(document, offset)):

- Precision@k = |R ∩ G| / |R|, and 0 if nothing is returned
- Recall@k = |R ∩ G| / |G|
- F1@k = 2·P·R/(P+R) per query (0 if P + R = 0), then averaged. This is the improvement loop's
  selection objective, **not** a benchmark metric.
- **k counts ranked passages, not characters.** If fewer than k passages match, P@k and R@k use
  the passages returned; nothing is padded. This happens for 8/140 train answerable queries at
  k = 5 in the final configuration.
- **Aggregation:** an unweighted mean over queries, with `n` reported for every aggregate.
- **Two views:**
  - "retrieval" uses the ranked list regardless of abstention (the benchmark view);
  - "with abstention" counts an abstained answerable query as an empty list (P = R = 0).

**Equivalence with the authors' formulation.** The LegalBench-RAG reference implementation
(public authors' code, not vendored here) sums pairwise overlaps between each retrieved snippet
and each gold snippet, without merging. This implementation uses interval unions instead. The two
are identical when (a) gold spans don't overlap, and (b) returned passages don't overlap.
- (a) holds for all 194 queries.
- (b) is guaranteed by the `skip`/`trim` overlap policies used by both the baseline and the final
  configuration.

A pairwise variant is computed alongside (`ref_precision@k`, `ref_recall@k`). It equals the
union-based value at every k in all six saved `metrics.json` files *(re-checked)*. Unit tests
(`tests/test_metrics.py`) cover exact and partial coverage, extra text, wrong document, multiple
gold spans, overlapping and duplicate passages, empty retrieval, k cutoffs and aggregation.

Unweighted per-query averaging is our reading of the authors' protocol; it isn't re-verified
against their code in this repository.

**Abstention metrics.**

| Metric | Definition |
|---|---|
| False-abstention rate | answerable queries abstained on / answerable queries |
| Correct-abstention rate | unanswerable queries abstained on / unanswerable queries |
| Failure-to-abstain rate | 1 − correct-abstention rate |
| Balanced accuracy | ½ · (answer rate on answerable + abstention rate on unanswerable) |

## 7. Baseline

[`configs/baseline.yaml`](configs/baseline.yaml):
- **Ranking:** BM25 of the **full** query over all 29 contracts; no routing.
- **Chunking:** 1,000/150-character chunks; overlap policy `skip`.
- **Text:** lowercase only; no stemming or stopwords.
- **Abstention:** `chunk_bm25_norm` (the best chunk's BM25 score ÷ the query's BM25 upper
  bound). The threshold, 0.2418, was calibrated on train and written into the config before its
  test run.

| k | Train P | Train R | Train F1 | Test P | Test R | Test F1 |
|---|---|---|---|---|---|---|
| 1 | 0.0028 | 0.0071 | 0.0040 | 0.0032 | 0.0185 | 0.0054 |
| 2 | 0.0070 | 0.0262 | 0.0110 | 0.0086 | 0.0438 | 0.0140 |
| 4 | 0.0158 | 0.1108 | 0.0264 | 0.0096 | 0.1278 | 0.0174 |
| 5 | 0.0191 | 0.1650 | 0.0328 | 0.0075 | 0.1278 | 0.0138 |
| 8 | 0.0183 | 0.2527 | 0.0330 | 0.0087 | 0.1668 | 0.0155 |
| 16 | 0.0116 | 0.2925 | 0.0219 | 0.0093 | 0.2470 | 0.0170 |
| 32 | 0.0072 | 0.3753 | 0.0140 | 0.0069 | 0.3254 | 0.0131 |
| 64 | 0.0043 | 0.4619 | 0.0084 | 0.0044 | 0.3779 | 0.0085 |

n = 140 train / 54 test answerable. Abstention: train false abstention 5/140, correct abstention
28/28; test false abstention 3/54, correct abstention 7/7.

Sources: `artifacts/eval/baseline_train_20261102-153419/metrics.json`,
`artifacts/eval/baseline_test_20261102-153427/metrics.json` *(re-checked)*.

## 8. Self-improvement loop and experimental methodology

**Mechanism** (`src/improvement_loop.py`, run with
`python -m src.cli improve --config configs/baseline.yaml --spec configs/loop.yaml --run-name <name>`):

1. **Data.** Test queries are removed from the dataset object before the loop starts, so only
   train answerable and train unanswerable queries exist inside the loop. The negative-set file
   is hashed, and the loop aborts if the hash changes.
2. **Baseline.** The baseline is evaluated on train (iteration 0); its abstention threshold is
   calibrated on train. It becomes the accepted configuration.
3. **Proposal.** Diagnostics label each train failure (§12). A rule-based proposer picks the first
   untried candidate whose `tags` include the accepted configuration's dominant failure category,
   otherwise the next candidate in queue order. All candidates are **predeclared** in
   [`configs/loop.yaml`](configs/loop.yaml), each with a written hypothesis.
4. **Evaluation.** The candidate's changes are applied on top of the **currently accepted**
   configuration, its threshold is re-calibrated on train, and it is evaluated on train.
5. **Acceptance rule** (declared in `configs/loop.yaml`, unchanged across runs):
   - the primary metric `retrieval.f1@5` must improve by ≥ 0.002;
   - **and** all guardrails must hold relative to the accepted configuration:
     - recall@5 drop ≤ 0.05
     - precision@1 drop ≤ 0.05
     - abstention balanced accuracy drop ≤ 0.05
     - offset errors = 0
6. **Logging.** Every candidate (accepted, rejected or skipped) is written to `iterations.jsonl`
   with its hypothesis, resolved changes, train metrics, guardrail checks, decision, reason,
   proposer, timestamp and git revision. `accepted_config.yaml` is written only on acceptance, so
   a rejected candidate can't replace it (this is tested).
7. **Selection.** The last accepted configuration of the final run is promoted to
   `configs/final.yaml`. Test evaluation happens only outside the loop, via
   `evaluate --split test --final-test`.

**Runs.** Three runs used the same protocol and code path, all on train only.

| Run | Spec | Change from previous spec | Data used for selection | Candidates evaluated (beyond baseline) | Accepted chain | Evidence available |
|---|---|---|---|---|---|---|
| 1 | v1 | — | train | 11 (+2 skipped: dense extra missing) | `stem_stopwords` → `doc_routing` → `doc_title_in_index` | `artifacts/loop/20261102-144050/` (complete) |
| 2 (original) | v2 | added `question_only_dual_abstention` | train | 12 *(session record only)* | ended at `doc_title_in_index` *(session record only)* | **overwritten**, see §9 |
| 2 (re-run) | v3 | added `question_only_fullquery_abstention` | train | 12 (+1 skipped) | `question_only_fullquery_abstention` → `stem_stopwords` → `overlap_trim` → `overlap_up` | `artifacts/loop/run2/` (complete) |
| 3 | v3 | none (same spec, same code) | train | 12 (+1 skipped) | same as run 2 re-run; identical decisions | `artifacts/loop/run3/` (complete) |

**Run 3 iterations**, train, from `artifacts/loop/run3/iterations.jsonl`. Iteration 0 is the
baseline; iterations 1–12 are 12 genuine evaluated candidates, each with its own configuration
and train evaluation:

| # | Candidate (hypothesis, abbreviated) | F1@5 | P@5 | R@5 | R@64 | P@1 | Bal. acc. | Decision (reason) |
|---|---|---|---|---|---|---|---|---|
| 0 | baseline | 0.033 | 0.019 | 0.165 | 0.462 | 0.003 | 0.982 | accepted (reference) |
| 1 | `question_only_chunk_query`: rank with the question inside the routed contract | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.807 | rejected (balanced-accuracy guardrail) |
| 2 | `question_only_dual_abstention`: same + two-threshold (contract and question) abstention | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.904 | rejected (balanced-accuracy guardrail) |
| 3 | `question_only_fullquery_abstention`: same ranking, full-query abstention signal | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.982 | **accepted** (+0.044) |
| 4 | `stem_stopwords` | 0.111 | 0.066 | 0.546 | 0.701 | 0.166 | 0.989 | **accepted** (+0.035) |
| – | `hybrid_rrf` | | | | | | | skipped (dense extra not installed) |
| 5 | `doc_routing` (resets to full-query chunk ranking) | 0.051 | 0.030 | 0.275 | 0.652 | 0.009 | 0.989 | rejected (−0.060) |
| 6 | `doc_title_in_index` | 0.109 | 0.064 | 0.539 | 0.695 | 0.164 | 0.989 | rejected (−0.003) |
| 7 | `chunk_500` | 0.142 | 0.092 | 0.452 | 0.606 | 0.237 | 0.961 | rejected (recall@5 guardrail) |
| 8 | `overlap_trim` | 0.126 | 0.075 | 0.621 | 0.878 | 0.166 | 0.989 | **accepted** (+0.015) |
| 9 | `overlap_up` (overlap 300) | 0.131 | 0.079 | 0.617 | 0.878 | 0.174 | 0.989 | **accepted** (+0.004) |
| 10 | `chunk_300` | 0.188 | 0.136 | 0.427 | 0.670 | 0.275 | 0.925 | rejected (recall@5 and balanced-accuracy guardrails) |
| 11 | `bm25_params` (k1 1.2, b 0.5) | 0.128 | 0.077 | 0.605 | 0.878 | 0.170 | 0.986 | rejected (−0.003) |
| 12 | `abstain_on_doc_signal` | 0.131 | 0.079 | 0.617 | 0.878 | 0.174 | 0.879 | rejected (no F1 gain) |

The run stopped at `max_iterations: 12`, so `chunk_1500` and `dense_only` weren't reached in the
spec-v3 runs. `chunk_1500` was evaluated, and rejected, in run 1.

**Run 1 iterations**, train, from `artifacts/loop/20261102-144050/iterations.jsonl`, summarised:

| # | Candidate | F1@5 | R@5 | P@1 | Bal. acc. | Decision |
|---|---|---|---|---|---|---|
| 0 | baseline | 0.0328 | 0.1650 | 0.0028 | 0.982 | accepted |
| 1 | `question_only_chunk_query` | 0.0766 | 0.4386 | 0.0965 | 0.807 | rejected (balanced-accuracy guardrail) |
| 2 | `stem_stopwords` | 0.0377 | 0.2136 | 0.0087 | 0.989 | accepted |
| 3 | `doc_routing` | 0.0512 | 0.2748 | 0.0087 | 0.989 | accepted |
| 4 | `doc_title_in_index` | 0.0550 | 0.2930 | 0.0087 | 0.989 | accepted |
| 5–11 | `chunk_500`, `overlap_trim`, `overlap_up`, `chunk_300`, `bm25_params`, `abstain_on_doc_signal`, `chunk_1500` | 0.038–0.055 | | | 0.879–0.989 | all rejected (F1 not improved by ≥ 0.002) |

**Why spec v2 and v3 were added** (change log in `configs/loop.yaml`):
- **v2, after run 1.** Run 1's train diagnostics showed that question-only ranking more than
  doubled F1@5. It failed the guardrail because a single chunk-level abstention signal could no
  longer reject queries naming nonexistent contracts.
- **v3, after the original run 2.** The two-threshold rule reached balanced accuracy 0.904, but
  the guardrail needed ≥ 0.939. It made 7 false abstentions, 4 of them on one contract (HPIL)
  whose header wording differs from the query preamble, and 4 failures to abstain, all on
  `unspecified_info` negatives (`artifacts/loop/run3/iter02_question_only_dual_abstention/`,
  *re-checked*).
- **Data used.** Both changes were motivated by **train** diagnostics only. Adding candidates
  between runs is a human-in-the-loop step outside the one-command loop, and is disclosed as
  such.

**Interpretation.**
- Small-chunk candidates (`chunk_500`, `chunk_300`) had the highest F1@5 but lost more than 0.05
  recall@5. The predeclared guardrail rejected them; a different objective would choose
  differently.
- Several accepted gains are small (+0.004 for `overlap_up`) and fall within the noise of 140
  queries.
- Each loop run took about 4 seconds (first and last timestamps in each `iterations.jsonl`).

## 9. Methodological deviations and evaluation integrity

**9.1 Negative-set commit ordering.**
- **Timing.** Loop run 1 began at 14:40:50 IST (first timestamp in
  `artifacts/loop/20261102-144050/iterations.jsonl`). The negative set was first committed at
  14:44:58 IST (`20e9cf4`). The requirement to commit before the loop was **not met** for run 1.
- **What is established.** Run 1's `summary.json` records SHA-256 `77d8b48ab6c6…` for the file it
  loaded. That equals the committed file and the hash recorded by runs 2 and 3. So run 1 used
  exactly the content that was later committed, and the content has never changed.
- **What is not established.** There is no Git-level proof of the file's state before 14:40, and
  nothing proves the authors of the set had seen no system output before writing it. The set was
  authored, and checked with lexical absence tests, before any loop run, but that rests on the
  session record, not an artifact.

**9.2 Repeated test-set evaluation.** `artifacts/test_runs.jsonl` records three test runs
*(re-checked)*:

| # | Time (IST) | Config | Fingerprint | Context |
|---|---|---|---|---|
| 1 | 14:42:30 | `provisional`: the baseline configuration with its train threshold | `d64c5b4f…` | during early runbook checks, after loop run 1 and before any final selection |
| 2 | 15:34:05 | `overlap_up` (final) | `3254f317…` | after the final selection commit `b4dbca3` (15:33:54) |
| 3 | 15:34:27 | `baseline` | `c41401f0…` | for the baseline-versus-final comparison |

- **What run #1 revealed.** Run #1's retrieval and abstention results are identical to run #3's
  at every k *(re-checked)*. Its config differs from the baseline only by a key added to the code
  later. So it revealed the baseline's test performance, and nothing about any candidate.
- **No test-driven changes in the record.** The loop can't read test data. Every later change
  (spec v2, v3) cites train diagnostics. No artifact records test results being used for a
  decision.
- **What can't be shown from artifacts.** That the developer didn't look at run #1's output. A
  single locked final evaluation would be the stronger protocol; three evaluations, one of them
  before final selection, are weaker even if no tuning followed.

**9.3 Overwritten experiment artifacts.**
- The original spec-v2 run used `--run-name run2`. Its directory was later overwritten by a
  re-run with spec v3 under the same name.
- Its results survive only in the development session record (§8 table: 12 evaluated,
  `question_only_dual_abstention` with F1@5 0.0766 and balanced accuracy 0.904, rejected).
- The same candidate was re-evaluated with identical code in the v3 runs and gave the same
  numbers. Still, the original v2 run's machine-readable log no longer exists.
- Runs 2 (re-run) and 3 used the same spec and produced identical decisions, which shows the
  loop is deterministic.

**9.4 Per-query outputs not in version control.** `.gitignore` excludes
`artifacts/**/per_query*.jsonl`. Aggregate metrics, configs, loop logs and train failure records
are committed. The per-query outputs behind the test metrics exist only in the local working
tree (about 0.4 MB per test run).

**9.5 Change made after the test runs.**
- **What changed.** After test runs #2/#3, an audit found that a question naming no contract was
  silently routed to an arbitrary best-matching contract. `query.require_contract: true` was
  added to `configs/final.yaml` (commit `0e4abd3`).
- **Why test results are unaffected.**
  - The flag can only change "answered" to "abstained", and only for queries without a preamble.
  - All 194 benchmark queries have a preamble, so no answerable result can change.
  - All 7 test negatives were already abstained, so none can change.

  The reported test metrics therefore hold for the updated configuration. **No fourth test run
  was made.**
- **Train check.** A train evaluation of the updated config with the stored threshold
  (`artifacts/eval/overlap_up_train_20261102-162333/`) reproduces loop run 3's iteration 9 at
  every k and on every abstention count *(re-checked)*.
- **Fingerprints.** The current `configs/final.yaml` has fingerprint `72c8f8c97f8f7ab1`. Removing
  the new key gives `3254f317b4c41e2c`, the tested configuration.

**9.6 Representativeness of the negative set.**
- 35 negatives, of which 7 are in test, and only about 7 realistic "answer absent from a real
  contract" cases (§4). They support only limited conclusions about abstention on real user
  questions.

**9.7 Gold/query consistency** (documented; no annotation was modified).
- **A8, Tate & Lyle / Igene, "minimum commitment".** The two gold spans are a capitalisation
  commitment of "at least $21,614,000" [13653, 13922] and an annual-dividend obligation
  [20181, 20459]. The second fits "minimum commitment" only loosely. This is a CUAD annotation
  choice, not a retrieval error.
- **Failure #11 (§12), BicycleTX, "right of first refusal / offer / negotiation".** The gold
  spans describe a share-option arrangement and share almost no vocabulary with the question.
  This may be a loose annotation.
- **A7, "Information System Associates / Rubicon".** This is **not** a mismatch. CUAD file names
  use the SEC filer (`DUOSTECHNOLOGIESGROUP,INC_…`), while the contract text reads "by and between
  Information  System Associates, Inc." (with a double space in the source) and mentions Rubicon
  133 times. The gold span is retrieved at rank 1.

## 10. Baseline-versus-final results

**Final configuration** ([`configs/final.yaml`](configs/final.yaml)):
- query split into preamble and question; question-only chunk ranking
- top-1 contract routing (file-name title + first 3,000 characters)
- stemming and stopword removal
- 1,000/300-character chunks; overlap policy `trim`
- abstention on `chunk_full_bm25_norm` ≥ 0.27386511 (train-calibrated)
- `require_contract: true`, added after the test runs (§9.5)

Sources: `artifacts/loop/run3/iter09_overlap_up/metrics.json` (train),
`artifacts/eval/overlap_up_test_20261102-153405/metrics.json` (test). Baseline sources as in §7.
All *(re-checked)*.

**Retrieval** (the ranked list, regardless of abstention). Each cell is P / R / F1.

| k | Train baseline | Train final | Test baseline | Test final |
|---|---|---|---|---|
| 1 | 0.0028 / 0.0071 / 0.0040 | 0.1745 / 0.4032 / 0.2228 | 0.0032 / 0.0185 / 0.0054 | 0.1788 / 0.4328 / 0.2147 |
| 2 | 0.0070 / 0.0262 / 0.0110 | 0.1246 / 0.4740 / 0.1818 | 0.0086 / 0.0438 / 0.0140 | 0.1495 / 0.5616 / 0.2044 |
| 4 | 0.0158 / 0.1108 / 0.0264 | 0.0881 / 0.5729 / 0.1416 | 0.0096 / 0.1278 / 0.0174 | 0.1063 / 0.6708 / 0.1647 |
| 5 | 0.0191 / 0.1650 / 0.0328 | 0.0787 / 0.6174 / 0.1306 | 0.0075 / 0.1278 / 0.0138 | 0.0947 / 0.7144 / 0.1514 |
| 8 | 0.0183 / 0.2527 / 0.0330 | 0.0614 / 0.6736 / 0.1073 | 0.0087 / 0.1668 / 0.0155 | 0.0696 / 0.7363 / 0.1167 |
| 16 | 0.0116 / 0.2925 / 0.0219 | 0.0457 / 0.7806 / 0.0835 | 0.0093 / 0.2470 / 0.0170 | 0.0432 / 0.7967 / 0.0786 |
| 32 | 0.0072 / 0.3753 / 0.0140 | 0.0379 / 0.8438 / 0.0700 | 0.0069 / 0.3254 / 0.0131 | 0.0328 / 0.8668 / 0.0619 |
| 64 | 0.0043 / 0.4619 / 0.0084 | 0.0358 / 0.8778 / 0.0663 | 0.0044 / 0.3779 / 0.0085 | 0.0280 / 0.8895 / 0.0533 |

n = 140 train / 54 test answerable queries. Offset errors are 0 in all four evaluations.

**With abstention** (abstained = empty list), final test: P@1 0.1603, R@1 0.4283, P@5 0.0875,
R@5 0.7049. Final train: P@1 0.1715, R@1 0.3976, P@5 0.0780, R@5 0.6118.

**Interpretation.**
- **Recall is much stronger than precision.** At k = 5 the final configuration's test recall is
  0.714, but its precision is 0.095: per query, on average under 10% of the returned characters
  are gold text. That follows from returned passages averaging about 785 characters (train,
  top 5) against gold spans with a median of 317 characters, with up to five passages returned.
- **High recall isn't a reliable legal answer.** The gold clause is often present somewhere in
  the five passages, and a user still has to find and read it.
- **Test above train.** Final test metrics are slightly higher than train (R@5 0.714 vs 0.617).
  With 54 queries over the same 29 contracts, that is within sampling variation and shows no
  overfitting signal. It isn't evidence of better generalisation.
- **Comparability.** Baseline and final use the same split, metric code and evaluation protocol.
  Thresholds were calibrated on train for each, separately, because their signals differ.

## 11. Abstention analysis

| | Answered | Abstained |
|---|---|---|
| Train answerable (140) — final | 137 | 3 (false abstention) |
| Train unanswerable (28) — final | 0 (failure to abstain) | 28 |
| Test answerable (54) — final | 53 | 1 (false abstention) |
| Test unanswerable (7) — final | 0 | 7 |
| Test answerable (54) — baseline | 51 | 3 |
| Test unanswerable (7) — baseline | 0 | 7 |

- **What the terms mean.**
  - A **false abstention** is refusing to answer when the contract does contain the answer; the
    user loses evidence that exists.
  - A **failure to abstain** is returning passages for a question the contracts can't answer; the
    user may wrongly treat them as evidence.
- **Small samples.** 7/7 correct abstentions on test is a very small sample. The Wilson 95%
  interval for the correct-abstention rate is **[0.646, 1.000]** (score interval with z = 1.96,
  computed from the counts above). For test false abstention, 1/54, it is [0.003, 0.098]; for
  train correct abstention, 28/28, it is [0.879, 1.000]. Perfect observed counts shouldn't be
  read as perfect abstention.
- **Threshold choice.**
  - **Rule.** Candidate thresholds are the minimum observed signal, the midpoints between
    consecutive distinct observed values, and the maximum + 1e-9, all on train. The one with the
    highest balanced accuracy is chosen; ties go to the smallest threshold.
  - **Scale.** Signals are normalised BM25 scores in [0, 1) and are not probabilities.
  - **Comparability.** Thresholds aren't comparable across configurations or signals; each
    configuration is calibrated separately.
- **Trade-off around the selected threshold.** These figures are computed from the saved train
  signals in `artifacts/loop/run3/iter09_overlap_up/per_query.jsonl`; no new evaluation was run.

  | Threshold | False abstentions (/140) | Failures to abstain (/28) | Bal. acc. |
  |---|---|---|---|
  | **0.2739 (selected)** | 3 | 0 | 0.989 |
  | 0.2600 | 3 | 1 | 0.971 |
  | 0.2500 | 2 | 3 | 0.939 |
  | 0.2470 | 1 | 3 | 0.943 |
  | 0.2400 | 0 | 3 | 0.946 |

  Three train negatives (`unans-026` 0.251, `unans-030` 0.257, `unans-025` 0.271) sit just below
  the threshold. All three are `unspecified_info` questions about real contracts, and the margin
  is thin.
- **No contract named** (`require_contract`). This is separate from low evidence. It reports
  reason `contract_not_identified` and suggests the three closest contracts, rather than implying
  that an arbitrary contract was meant.

## 12. Failure analysis

**Categories.** Failures are categorised on train with the final configuration at k = 5
(`src/diagnostics.py`; categories in priority order: offset error, false abstention, wrong
document, wrong section, chunk boundary, partial span, low rank, irrelevant extra).

**Counts** (`artifacts/error_analysis/overlap_up/summary.json`, 140 answerable):

| Category | Count |
|---|---|
| ok | 24 |
| wrong section | 43 |
| irrelevant extra | 37 |
| low rank | 15 |
| partial span | 11 |
| chunk boundary | 7 |
| false abstention | 3 |
| wrong document | 0 |
| offset error | 0 |

The 28 unanswerable queries were all abstained correctly. For the baseline
(`artifacts/error_analysis/baseline/summary.json`): wrong section 104, low rank 13, chunk
boundary 13, false abstention 5, partial span 4, irrelevant extra 1, ok 0.

**Twelve failures.** All are from train, final configuration, and appear in
`artifacts/error_analysis/overlap_up/failures.jsonl` with the stated category and metrics
*(re-checked)*. Offsets are `[start, end)`. Causes are hypotheses unless stated otherwise. **No
listed remediation was implemented or measured** unless noted.

| ID | Query (contract; question) | Expected evidence | Actual | Category | Likely cause | Proposed remediation |
|---|---|---|---|---|---|---|
| 1 `cuad-551a572623` | BicycleTX/Crockett; exceptions to competitive restrictions | [33572, 34034] "save that nothing in this paragraph 13.2 shall prevent you…" | #1 [37817, 38817], #2 [38817, 39508]: the covenants themselves; R@5 = 0 | wrong section | lexical overlap rewards the restriction, not its carve-out ("save that") | reranker; carve-out query expansion |
| 2 `cuad-0b7b50dadf` | HPIL/GINARES; expiration date | [5604, 5739] "The term of this Agreement shall be one (1) year…" | #1 [7739, 8739], insolvency boilerplate (score 2.37); R@5 = 0 | wrong section | vocabulary gap (expiration ↔ term) | dense/hybrid retrieval (implemented, not evaluated) |
| 3 `cuad-e5b265c6b3` | BicycleTX; governing law | [53956, 54252] "…governed by… the laws of England…" | inside #1 [53459, 54272]; P@5 = 0.071, R@5 = 1.0 | irrelevant extra | 296-character answer within about 4,200 returned characters (296 / 0.071) | sentence-level refinement; smaller chunks under a recall-aware objective |
| 4 `cuad-cc22d5d0ab` | HPIL; governing law | [16867, 17117] | inside #1 [16376, 17340]; #2 is the table of contents [1775, 2741]; P@5 = 0.059 | irrelevant extra | table-of-contents headings match clause names | down-weight table-of-contents chunks |
| 5 `cuad-5c06b5a634` | ISA/Rubicon; exceptions to competitive restrictions | [23556, 23770] | #1 [20522, 21517], #2 [22344, 23093] (the non-compete); gold lower in the top 5; P@5 = 0.059 | low rank | carve-out ranked below the restriction it modifies | reranker |
| 6 `cuad-92c250e51b` | Florida Chemical/Flotek; duration of warranties | [3021, 3209] "FCC shall promptly, but in no event later than three (3) days…" | #1 [13245, 14220] (termination); gold reached via #2 [2383, 3209]; P@5 = 0.046 | low rank | annotated answer never says "warranty" | dense/hybrid retrieval |
| 7 `cuad-e568fcd380` | ISA/Rubicon; IP ownership assignment | [14401, 14603], [14605, 15442] | #1 [13158, 14127], #2 [17453, 18445] (neighbouring IP clauses); R@5 = 0.112 | partial span | many IP-dense sections compete; the long definitional span isn't ranked | adjacent-chunk expansion; reranker |
| 8 `cuad-9d8033e4f6` | Premier Biomedical; exclusivity | [3388, 4736], [12938, 13072] | #1 [1193, 2132]: a WHEREAS recital mentioning "Exclusive License"; R@5 = 0.107 | partial span | recitals repeat key terms more densely than operative clauses | down-weight recitals |
| 9 `cuad-eb238d491d` | ISA/Rubicon; exclusivity | [5690, 6079], [6537, 7080] | #2 [6776, 7377] (start set by overlap trimming) covers only the tail of the second span; R@5 = 0.592 | chunk boundary | the trimmed remainder begins mid-clause | clause-numbering-aware splitting |
| 10 `cuad-dd123231af` | ISA/Rubicon; licenses granted | [5690, 6080], [6537, 7080] | #1 [13158, 14127], #2 [14127, 14604] (IP reservation); R@5 = 0.581 | chunk boundary | licence grant split across chunks and outranked | clause-aware splitting; reranker |
| 11 `cuad-2f7d42bc6c` | BicycleTX; right of first refusal/offer/negotiation | [6235, 6531], [6533, 7937] (share-option text) | abstained (signal 0.245 < 0.2739); raw ranking also had R@5 = 0 | false abstention | question/gold vocabulary mismatch; possibly a loose annotation (§9.7) | none on the retrieval side; flag the annotation |
| 12 `cuad-7646cba011` | BicycleTX; IP ownership assignment | [44840, 45359] | abstained (signal 0.248), although raw #1 [44251, 45248] covered 408/519 gold characters (R@5 = 0.786) | false abstention | full-query normalised score is low for this long contract; routing and ranking were correct (*verified*) | better-calibrated signal on train; **not** a lower threshold (§11 trade-off) |

**Reported cases checked in the audit** (train queries; `configs/final.yaml`):

| Case | Finding | Classification |
|---|---|---|
| E1 (= failure #12) | false abstention; the cause is the abstention threshold, *verified* (§11) | genuine failure |
| E2: "What is the governing law for this contract?" with **no contract named** | Previously answered from the HPIL contract by silent routing. Now abstains with `contract_not_identified` and suggestions; regression tests in `tests/test_retrieval.py`. Previous descriptions of E2 as "a contract that was not available" were inaccurate: the query names no contract. | design defect, fixed after the test runs (§9.5) |
| E3: "Papa John's … and its endorser", governing law | answered; #1 [63073, 63864] contains the Delaware clause [63649, 63806] | not a failure |
| A3: Walabot reseller, liability cap | gold [11885, 12465] covered by #1 (65 characters) + #2 (515 characters); recall@2 = 1.0 | display splitting across contiguous chunks, not missing evidence |
| A4: Depomed/King, audit rights | two gold spans fully covered by ranks 1–3 | same as A3 |
| A7: ISA/Rubicon, renewal term | correct contract mapping (§9.7); gold [18727, 19214] at rank 1 | not a failure |
| A8: Tate & Lyle/Igene, minimum commitment | second gold span at rank 1; loose annotation (§9.7); `demo-check` samples a different question for this contract | annotation-consistency note |

## 13. Limitations and future work

**Observed limitations.**
- **Low precision:** returned passages average about 785 characters, against 317-character
  median gold spans (§10). Smaller chunks failed the recall guardrail.
- **Lexical ranking:** vocabulary gaps and carve-out phrasing cause most wrong-section and
  low-rank failures (§12).
- **Routing:**
  - it depends on a "Consider …;" preamble;
  - routing is top-1, so a wrong routing decision would give zero recall (none occurred on
    train);
  - free-form contract references aren't resolved.
- **Abstention:** the threshold sits close to three realistic train negatives (§11). Test
  evidence for abstention comes from 7 queries.
- **Scope:** 29 contracts shared across splits; the results don't establish performance on
  unseen contracts.
- **Protocol deviations:** see §9.

**Proposed future work** (none of this was implemented or measured):
- sentence-level refinement of top passages;
- evaluating the implemented dense/hybrid retrievers, and a cross-encoder reranker;
- down-weighting recitals and table-of-contents chunks;
- clause-numbering-aware chunk boundaries;
- a length-aware abstention signal;
- a larger, independently authored negative set focused on real-contract absent-information
  questions;
- multi-contract retrieval for queries that don't name a contract;
- a single locked test evaluation.

## 14. Reproducibility

Run the following commands from the repository root.

```bash
# Install dependencies and activate the environment
uv sync && source .venv/bin/activate

# Prepare benchmark data (requires cuad.json and corpus/cuad)
python -m src.cli prepare-data --source /path/to/legalbench-rag

# Validate prepared data
python -m src.cli validate-data  # expect VALIDATION OK

# Run automated tests
python -m pytest -q

# Evaluate baseline on the training split (re-calibrates abstention threshold)
python -m src.cli evaluate --config configs/baseline.yaml

# Run the train-only improvement loop
python -m src.cli improve --config configs/baseline.yaml --spec configs/loop.yaml --run-name reproduction_run_01

# Evaluate final configuration on the training split
python -m src.cli evaluate --config configs/final.yaml --no-calibrate

# Evaluate final configuration on the held-out test split
python -m src.cli evaluate --config configs/final.yaml --split test --final-test

# Evaluate baseline configuration on the held-out test split
python -m src.cli evaluate --config configs/baseline.yaml --split test --final-test

# Generate error analysis for the final configuration
python -m src.cli error-analysis --config configs/final.yaml
```

Use a unique run name for each reproduction run to avoid overwriting or confusing existing experiment artifacts.

**Evaluation note:** The test-set commands trigger held-out evaluations. Test results must not be used for configuration selection, threshold calibration, or improvement-loop decisions. The commands above describe a fresh reproduction workflow; they do not imply that the original experiments followed this exact sequence. Preserve the submitted historical experiment artifacts when reproducing the results.
**Inputs.**
- Python ≥ 3.13; dependencies pinned in `uv.lock`.
- The LegalBench-RAG `benchmarks/cuad.json` and `corpus/cuad/`.
- `data/unanswerable_queries.json`.

**Outputs.**
- `artifacts/eval/<config>_<split>_<timestamp>/`
- `artifacts/loop/<run>/`
- `artifacts/error_analysis/<config>/`
- `artifacts/test_runs.jsonl`, which is appended to, so any new test run increments the count.

**Determinism.** Everything is deterministic: no random sampling, and tie-breaking is explicit.
Loop runs 2 (re-run) and 3 produced identical decisions. A clean reproduction with spec v3
should reproduce `artifacts/loop/run3/`.

**What can't be reproduced as a historical artifact.**
- The original spec-v2 run (§9.3). Re-running with v2 would require restoring that spec version
  from Git history.
- Per-query test outputs are not committed (§9.4).

**Provenance.**

| Item | Value |
|---|---|
| Tested final config fingerprint | `3254f317b4c41e2c` (= `artifacts/loop/run3/accepted_config.yaml`) |
| Current `configs/final.yaml` fingerprint | `72c8f8c97f8f7ab1` (= tested + `require_contract: true`) |
| Final selection commit | `b4dbca3` (test runs #2/#3 followed it) |
| Post-test audit commit | `0e4abd3` |
| `cuad.json` / manifest / negative set SHA-256 | `8e0405b15fb8…` / `204a4d7efb3a…` / `77d8b48ab6c6…` |

Fingerprints are SHA-256 hashes of the fully resolved config (defaults merged), excluding `name`
and `status`. They are comparable only within one code version, because adding a config key
changes them.

## 15. AI tool usage

- **Tool.** Development used **Claude Code** (Anthropic) as an AI coding assistant. The session
  metadata identifies the model as Claude Opus 5.5.
- **Drafted with the assistant,** under the developer's direction:
  - most of the source code, tests and configurations;
  - the unanswerable-query set, including its lexical absence checks;
  - the documentation.
- **Run by the developer locally:** dependency installation, data preparation, all evaluations,
  all loop runs and all test-split runs. The developer shared the outputs back for analysis.
- **Design changes made during development** were proposed from train diagnostics and are
  documented in §8:
  - question-only ranking with full-query abstention;
  - contract-identity abstention;
  - the stopword-only guard.
- **Responsibility.** The developer is responsible for understanding, explaining and maintaining
  the implementation.

## 16. Conclusion

- **What was implemented.** An offset-exact, deterministic BM25 retrieval system for the
  prescribed CUAD mini benchmark, with contract routing, train-calibrated abstention, the
  benchmark's character-level metrics (verified equivalent to the authors' pairwise formulation
  under invariants that hold here), a logged train-only improvement loop, a CLI and a web app.
- **What the results show.** On the held-out split, the selected configuration retrieves most
  gold text within five passages (R@5 0.714 vs 0.128 for the baseline). Its abstention rejected
  all 7 test negatives with one false abstention in 54.
- **What they don't show.**
  - Precise evidence extraction: P@5 is 0.095.
  - Reliable abstention beyond this small, partly easy negative set.
  - Performance on contracts outside these 29.
  - A fully clean protocol: the negative set was committed after the first loop run started, the
    test split was run three times, one historical loop run is only in the session record, and
    one configuration change was made after testing (shown not to affect the benchmark results).
- **Biggest technical gaps.** Precision, and lexical vocabulary gaps.
