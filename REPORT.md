# Contract Intelligence Assistant — Technical Report

**Evidence conventions.** Every number comes from a repository artifact, cited by path. Values
re-extracted from those artifacts during the final documentation audit are marked
*(re-checked)*. Facts known only from the development session's console output, with no saved
artifact, are marked *(session record only)*. No test-split evaluation was run during the audit.

**Naming note (2026-11-06).** `configs/candidate_v4.yaml` was promoted to `configs/final.yaml`
(§14). In §2–§13, written before the promotion, "final" and `configs/final.yaml` mean the
**previous** final configuration `overlap_up`, now kept unchanged at
`configs/archive/final_overlap_up.yaml`. To reproduce a command from those sections, substitute
that path.

## 1. Executive summary

**What was built.**
- A deterministic retrieval system that returns verbatim contract passages with exact
  `[start, end)` character offsets, or abstains when the evidence is insufficient.
- In the final configuration (`configs/final.yaml`, promoted from `candidate_v4`, §14):
  - each query's contract preamble routes it to one contract;
  - BM25 ranks that contract's chunks using the question alone, with generic template words
    removed and a controlled clause vocabulary added at half weight (§11);
  - a normalised BM25 score of the full, unmodified query, with a train-calibrated threshold,
    decides abstention.
- No LLM is used at inference time.

**Benchmark.**
- LegalBench-RAG-mini, CUAD subset: 194 queries over 29 contracts, split by the prescribed
  SHA-256 rule into 140 train / 54 test.
- 35 hand-authored unanswerable queries (28 train / 7 test).

**Test evaluations.** Nine test evaluations were recorded in total (`artifacts/test_runs.jsonl`):

| # | Config | Role |
|---|---|---|
| 1 | provisional | an early run, equivalent to the baseline, made before any final selection |
| 2 | `overlap_up` | the previous final configuration |
| 3 | baseline | the comparison point |
| 4 | `overlap_up` | reproduction check (identical results to #2) |
| 5 | `candidate_v4` | **the current final configuration** (promoted after this run, §14) |
| 6–8 | verifier rescue, MiniLM reranker, gte reranker | reporting runs for experiments already rejected or not promoted on train (§14) |
| 9 | `final_v4` (promoted `configs/final.yaml`) | confirmation run; identical to #5 |

Runs #1–#3 are documented in §10, runs #4–#9 in §14.

**Held-out test results** *(sources:* `artifacts/eval/baseline_test_20261102-153427/`,
`artifacts/eval/overlap_up_test_20261102-153405/`, `artifacts/eval/cmp_test_B_candidate_v4/`,
each `metrics.json`*)*:

| Test metric (54 answerable / 7 unanswerable) | Baseline | Previous final (`overlap_up`) | **Final (`candidate_v4`)** |
|---|---:|---:|---:|
| precision@1 | 0.0032 | 0.1788 | **0.2638** |
| recall@1 | 0.0185 | 0.4328 | **0.5880** |
| precision@5 | 0.0075 | 0.0947 | **0.1011** |
| recall@5 | 0.1278 | 0.7144 | **0.7821** |
| F1@5 (selection objective) | 0.0138 | 0.1514 | **0.1607** |
| recall@64 | 0.3779 | 0.8895 | **0.9612** |
| false abstentions (answerable) | 3/54 | 1/54 | 1/54 |
| correct abstentions (unanswerable) | 7/7 | 7/7 | 7/7 |
| balanced abstention accuracy | 0.972 | 0.991 | 0.991 |
| offset errors | 0 | 0 | 0 |

**Main improvements.**
- Most of the gain over the baseline came from separating *which contract* (routing by the
  preamble) from *where in the contract* (ranking by the question). In the baseline, party names
  pulled the top passage to the contract header in 124/140 train queries.
- The promoted query refinement (§11) then raised test recall@1 from 0.433 to 0.588 with
  abstention unchanged.

**Remaining weaknesses.**
- Precision is low: P@5 = 0.101 on test, so about 10% of the returned characters are gold text.
- 9/54 test questions, mostly "is there a … clause" questions, have no gold text in the top 5.
- Cross-encoder reranking and an LLM evidence verifier were tested and did not help (§12–§14).

**Protocol caveats** (§10, §14.4):
- the test split was evaluated nine times, and the final configuration was promoted after
  seeing its test result (run #5);
- the unanswerable set was committed about four minutes after the first loop run started;
- the original spec-v2 loop run survives only in console output.

**Query refinement, now final** (§11, §14). A later train-only loop run (run 4) accepted
`configs/candidate_v4.yaml`: generic-term removal plus controlled query expansion for the ranking
query. On train, F1@5 rose from 0.1306 to 0.1743 and recall@5 from 0.6174 to 0.8095, with
abstention unchanged (3/140 false, 28/28 correct), and demo group A went from 4/10 to 8/10. A
single-change ablation (§11.7) confirms that the gain comes from combining both changes. On test
(run #5) it also beat the previous final on every retrieval metric, and it was promoted to
`configs/final.yaml` on 2026-11-06 (§14).

## 2. System design

### 2.1 Pipeline (final configuration)

```
query
 ├─ split_query (src/text.py): "Consider <preamble>; <question>"  — query text only
 ├─ contract selection (src/retrieval.py: Index.retrieve)
 │    explicit document_id ───────────────────────► that contract
 │    preamble present ─► BM25 over [file-name title + first 3,000 chars] ─► top-1 contract
 │    no preamble + require_contract ─► abstain "contract_not_identified" + 3 suggestions
 ├─ ranking: BM25 of the QUESTION over the selected contract's chunks; ties by (−score, chunk_id)
 ├─ overlap policy "trim": a chunk overlapping an already-selected passage of the same contract
 │    is cut to its largest uncovered piece (dropped if < 50 chars)
 ├─ abstention signal: BM25 of the FULL query over the same chunks (chunk_full_bm25_norm)
 │    abstain iff no candidates, or signal < 0.27386511 (train-calibrated); equality answers
 └─ output: passages with exact offsets (re-checked against the source in src/pipeline.py)
```

`Pipeline.search` (`src/pipeline.py`) is the single entry point for the CLI, the Streamlit app
and evaluation; evaluation uses `Pipeline.retrieve` plus the same `decide()` rule. CLI and app
parity is tested in `tests/test_end_to_end.py`.

### 2.2 Components

**Loading.** CUAD contracts are plain-text files read with `open(path, encoding="utf-8").read()`
and never modified (`src/data.py`).

**Chunking** (`src/chunking.py`).
- Windows of at most `max_chars` characters.
- Each window's end moves back to the best boundary in its last 30%: paragraph break, then
  sentence end, then whitespace.
- The next window starts `overlap_chars` before the previous end, moved forward to a word start.
- The invariant `source[start:end] == text` is enforced and tested.

| Config | `max_chars` / `overlap_chars` | Chunks | Evidence |
|---|---|---|---|
| baseline | 1,000 / 150 | 1,617 | `validate-data` (default config `configs/baseline.yaml`, `src/cli.py`) |
| final | 1,000 / 300 | 2,027 (mean 889 chars) | `artifacts/index/8d4a7984b2102b7b/stats.json`; the fingerprint equals `index_fingerprint(configs/final.yaml)` *(re-checked)* |

**BM25** (`src/retrieval.py: BM25`).
- Okapi BM25 with k1 = 1.5 and b = 0.75; non-negative idf `ln(1 + (N − df + 0.5)/(df + 0.5))`;
  sums over unique query terms.
- Implemented in-house so that scoring can be restricted to one contract, the abstention
  normaliser is exact, and tie-breaking is explicit.
- Checked against a hand-computed value in `tests/test_retrieval.py`.
- Search-side text is lowercased, stopword-filtered and Snowball-stemmed (final config only).
  Source text is untouched.

**Routing and question-only ranking.**
- CUAD queries carry a preamble naming the agreement and its parties. That is a strong signal of
  *which* contract, but a poor signal of *where* the answer is.
- With the full query, party names dominate chunk scores: in the baseline, 124 of 140 train
  top-1 passages lay in a contract's first 3,000 characters *(re-checked,
  `artifacts/loop/20261102-144050/iter00_baseline/per_query.jsonl`)*.
- So the preamble is used only for routing, and the question alone ranks chunks.
- Routing chose a gold contract for 140/140 train queries in the final configuration
  *(re-checked, `artifacts/loop/run3/iter09_overlap_up/per_query.jsonl`)*.

**Abstention signal.**
- `chunk_full_bm25_norm` is the best BM25 score of the **full** query over the routed contract's
  chunks, divided by Σ idf(t)·(k1+1) over unique query terms. Out-of-vocabulary terms count with
  df = 0.
- So made-up party names and absent topics lower the score. It lies in [0, 1) and is not a
  probability.
- It is deliberately separate from the ranking query: §7 shows that a question-only abstention
  signal could not reject queries about nonexistent contracts.

**Contract identity** (`query.require_contract`). A question without a preamble, and with no
explicit `document_id`, is not routed to an arbitrary contract. It abstains with reason
`contract_not_identified` and three suggestions. This was added after the test evaluations
(§10.5).

**Output fields** (`src/retrieval.py: Passage`):

| Field | Meaning |
|---|---|
| `rank` | 1-based position after overlap handling |
| `document_id` | benchmark file path, e.g. `cuad/<file>.txt` |
| `start_offset`, `end_offset` | half-open Python string indices into the source text |
| `text` | `source[start_offset:end_offset]`, exactly |
| `score` | BM25 score of the ranking query |
| `chunk_id` | internal chunk identifier |

Search results also carry `abstained`, `abstention_reason`, `signal`, `signal_value`,
`threshold`, `document_filter` and `contract_candidates`.

**Implemented but not evaluated.**
- Dense retrieval (sentence-transformers `all-MiniLM-L6-v2`) and hybrid reciprocal-rank fusion
  exist behind the optional `dense` extra and are tested only with a stub encoder.
- They were never evaluated: the loop logged them as `skipped`, because the dependency wasn't
  installed.
- Neither the baseline nor the final configuration uses them.

## 3. LLM usage

No LLM, embedding model or learned reranker is used by the evaluated retrieval system. Source
inspection found no LLM client in `src/` or `app.py`. No model was trained or fine-tuned.

**Why deterministic lexical retrieval:**
- The task is to return exact evidence spans with offsets; BM25 does this directly and
  deterministically.
- It runs on CPU with no API keys, and sends no contract text to an external service.
- Every ranking and abstention decision can be explained.

An LLM or cross-encoder reranker is a candidate for future work on the dominant wrong-section
failures (§8). It wasn't tested. Claude Code was used as a development tool; see README.md
§AI-tool usage.

## 4. Evaluation setup

### 4.1 Dataset, selection and split

| Step | Implementation | Verified result |
|---|---|---|
| benchmark | `benchmarks/cuad.json` | 4,042 tests; SHA-256 `8e0405b15fb8…`, matching the dataset `SHA256SUMS` |
| mini selection | `src/data.py: mini(tests, n=194)`: sorted by `random.seed(t["snippets"][0]["file_path"]); random.random()`, first 194 | 194 queries |
| referenced contracts | the set of `snippets[*].file_path` (`referenced_documents`) | 29; indexed set == referenced set |
| split | `assign_split`: `h = int(sha256(query.strip().encode("utf-8")).hexdigest(), 16)`; `test if h % 10 < 3 else train` | 140 train / 54 test; agrees with the prescribed function for all 229 queries *(re-checked)* |
| gold validation | `document[start:end] == answer` on the decoded source | 272/272 spans match; no query has overlapping gold spans *(re-checked)* |

- The only preprocessing before hashing is `str.strip()`, which is part of the rule. Unanswerable
  queries use the same function.
- Offsets are Python string indices under default text-mode reading (universal newlines).
- The latest author-run `validate-data` reported `VALIDATION OK` with the counts above.
- The split is deterministic but doesn't separate contracts: all 29 contracts and the question
  templates appear in both splits. Test results therefore measure new (contract, question)
  pairs, not unseen contracts.

### 4.2 Unanswerable-query set

[`data/unanswerable_queries.json`](data/unanswerable_queries.json) (v1.0, SHA-256
`77d8b48ab6c6…`; 35 queries, 28 train / 7 test *(re-checked)*):

| Category | n | Kind of absence | Example |
|---|---:|---|---|
| `absent_topic` | 13 | topic not covered by any indexed contract | "What cryptocurrency or blockchain token is used to settle payments under this contract?" |
| `nonexistent_contract` | 11 | contract or party not indexed; one hard case names the real Papa John's with the wrong endorser | "Consider the Lease Agreement between Quillon Properties LLC and Marrowgate Foods Inc.; What is the monthly rent…?" |
| `unspecified_info` | 6 | a **real** indexed contract that doesn't state the requested information | "Consider the Non-Competition Agreement of Western Copper; What is the current copper price on the London Metal Exchange?" |
| `off_domain` | 5 | general knowledge | "Who won the FIFA World Cup in 2018?" |

**Checks.**
- Every query has a rationale and `absence_check_terms`.
- `validate-data` confirms that no check term occurs (case-insensitively) in any indexed
  contract, and that IDs and texts are unique and distinct from benchmark queries.

**Limitations.**
- **Lexical checks.** They can't prove semantic absence.
- **Few realistic negatives.** Only the 6 `unspecified_info` queries and the Papa John's case are
  realistic "plausible question, answer absent from a real contract" negatives. The others
  contain words absent from the corpus, which the BM25 signal is designed to penalise.
- **A borderline query.** `unans-011` (immigration petitions) sits near a "right to work in the
  United Kingdom" clause in two service agreements. It is unanswerable as written but harder than
  intended; it was left unchanged because the set is frozen.
- **Small test portion.** Only 7 negatives are in test (4 without a preamble, 3 with one).
- **Authorship.** The set was written by the developer with an AI assistant and wasn't
  independently reviewed.

### 4.3 Retrieval metrics (`src/metrics.py`)

For a query, let G be the set of gold characters and R the union of characters covered by the
first k returned passages, with characters identified by (document, offset):

- **precision@k** = |R ∩ G| / |R|, and 0 if nothing is returned
- **recall@k** = |R ∩ G| / |G|
- **F1@k** = 2PR/(P+R) per query (0 if P + R = 0). This is the loop's selection objective, not a
  benchmark metric.
- **k** counts ranked passages, not characters. If fewer than k passages match, the returned
  passages are scored without padding. At k = 5 this happens for 8/140 train answerable queries
  in the final configuration *(re-checked)*.
- **Aggregation:** unweighted mean over queries, with `n` reported for every aggregate.
- **Views:**
  - *retrieval*: the ranked list regardless of abstention (the benchmark view);
  - *with abstention*: an abstained answerable query counts as an empty list (P = R = 0).

**Equivalence to the authors' formulation.** The LegalBench-RAG reference code (public, not
vendored here) sums pairwise overlaps between each retrieved snippet and each gold snippet,
without merging. That is identical to the interval-union definition when (a) gold spans don't
overlap, and (b) returned passages don't overlap.
- (a) holds for all 194 queries.
- (b) is guaranteed by the `skip` (baseline) and `trim` (final) overlap policies.

The pairwise variant is computed alongside (`ref_precision@k`, `ref_recall@k`). It equals the
union value at every k in all six saved `metrics.json` files *(re-checked)*. Unit tests in
`tests/test_metrics.py` cover exact and partial coverage, extra text, wrong document, multiple
gold spans, overlapping and duplicate passages, empty retrieval, k cutoffs and aggregation.

Per-query unweighted averaging is our reading of the authors' protocol; it isn't re-verified
against their code here.

### 4.4 Abstention metrics

| Metric | Definition |
|---|---|
| false-abstention rate | abstained answerable / answerable |
| correct-abstention rate | abstained unanswerable / unanswerable |
| failure-to-abstain rate | 1 − correct-abstention rate |
| balanced abstention accuracy | ½ · (answer rate on answerable + abstention rate on unanswerable) |

## 5. Baseline versus final results

### 5.1 Configurations

| Setting | Baseline (`configs/baseline.yaml`) | Final (`configs/final.yaml`) |
|---|---|---|
| query use | full query everywhere | preamble → routing; question → ranking; full query → abstention |
| contract routing | none (all 29 contracts) | top-1 contract (file-name title + first 3,000 chars) |
| chunks | 1,000 / 150 chars | 1,000 / 300 chars |
| overlap policy | `skip` | `trim` |
| text normalisation | lowercase | lowercase + stopwords + Snowball stemming |
| abstention signal / threshold | `chunk_bm25_norm` ≥ 0.2418 | `chunk_full_bm25_norm` ≥ 0.2739 |
| `require_contract` | off | on (added after the test evaluations, §10.5) |

Both thresholds were calibrated on train for their own configuration, because the signals
differ.

### 5.2 Retrieval metrics (no abstention applied)

Each cell is P / R / F1. n = 140 train and 54 test answerable queries. Sources:
- train: `artifacts/eval/baseline_train_20261102-153419/metrics.json` and
  `artifacts/loop/run3/iter09_overlap_up/metrics.json`;
- test: as in §1.

All *(re-checked)*.

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

Offset errors are 0 in all four evaluations.

The author's latest train evaluation of the current `configs/final.yaml`
(`evaluate --no-calibrate`, `artifacts/eval/overlap_up_train_20261102-162333/`) reproduces the
train-final column exactly, including the abstention counts.

### 5.3 Retrieval metrics with abstention applied (abstained = empty list)

| | precision@1 | recall@1 | precision@5 | recall@5 |
|---|---:|---:|---:|---:|
| train final (n = 140) | 0.1715 | 0.3976 | 0.0780 | 0.6118 |
| test final (n = 54) | 0.1603 | 0.4283 | 0.0875 | 0.7049 |
| test baseline (n = 54) | 0.0032 | 0.0185 | 0.0075 | 0.1278 |

### 5.4 Abstention outcomes

| Split / config | Answerable: answered | Answerable: abstained | Unanswerable: abstained | Unanswerable: answered | Balanced acc. |
|---|---:|---:|---:|---:|---:|
| train baseline | 135 | 5 | 28 | 0 | 0.982 |
| train final | 137 | 3 | 28 | 0 | 0.989 |
| test baseline | 51 | 3 | 7 | 0 | 0.972 |
| test final | 53 | 1 | 7 | 0 | 0.991 |

- **What the terms mean.**
  - A *false abstention* withholds evidence that exists.
  - A *failure to abstain* presents passages for a question the contracts can't answer.
- **Wilson 95% score intervals** (z = 1.96, computed from the counts above):

  | Rate | Count | Interval |
  |---|---|---|
  | correct abstention, test final | 7/7 | [0.646, 1.000] |
  | false abstention, test final | 1/54 | [0.003, 0.098] |
  | correct abstention, train final | 28/28 | [0.879, 1.000] |

- **Limited evidence.** Seven test negatives can't establish abstention performance in general;
  7/7 is consistent with a true rate as low as about 65%.

### 5.5 Interpretation

- **Recall is much stronger than precision.** Final test recall@5 is 0.714, but precision@5 is
  0.095: on average under 10% of the returned characters are gold text.
  - Returned top-5 passages average about 785 characters (train, final config; computed from
    `artifacts/loop/run3/iter09_overlap_up/per_query.jsonl`).
  - Gold spans have a median of 316.5 characters.
- **Recall isn't answer correctness.** It measures gold characters contained somewhere in the
  returned passages. It isn't the share of questions answered correctly, and a reader still has
  to find the clause.
- **Test above train.** Final test metrics are slightly above train (recall@5 0.714 vs 0.617).
  With 54 queries over the same 29 contracts, this is within sampling variation; it isn't
  evidence of better generalisation.
- **Comparability.** Baseline and final use the same split, metric code and protocol.

## 6. Improvement-loop objective and guardrails

**Declaration.** The rule was declared in [`configs/loop.yaml`](configs/loop.yaml) before any loop
run, and the `protocol` block was the same in all runs:

| Rule | Value |
|---|---|
| primary metric | `retrieval.f1@5` on train; accept only if it improves by ≥ 0.002 (absolute) |
| guardrail | recall@5 must not drop by more than 0.05 vs the accepted config |
| guardrail | precision@1 must not drop by more than 0.05 |
| guardrail | balanced abstention accuracy must not drop by more than 0.05 |
| guardrail | offset errors = 0 |
| iterations | `max_iterations: 12`, `min_iterations: 5` |

**Mechanism** (`src/improvement_loop.py`):

1. **Train-only data.** Test queries are removed from the dataset object before the loop starts,
   and the negative-set file is SHA-256-hashed; the loop aborts if the hash changes.
2. **Baseline (iteration 0).** It is evaluated on train with its threshold calibrated on train,
   and becomes the accepted configuration.
3. **Proposal.**
   - Train diagnostics label every failure.
   - A **deterministic rule-based proposer** picks the first untried candidate whose `tags`
     include the accepted configuration's dominant failure category; otherwise it takes the next
     candidate in queue order.
   - Every candidate, with its written hypothesis, is predeclared in `configs/loop.yaml`.
4. **Evaluation.** The candidate's changes are applied on top of the **accepted** configuration,
   its threshold is re-calibrated on train, and it is evaluated on train.
5. **Decision and logging.** Each candidate (accepted, rejected or skipped) is logged in
   `iterations.jsonl` with its hypothesis, resolved changes, metrics, guardrail checks,
   decision, reason, proposer, timestamp and git revision. `accepted_config.yaml` is rewritten
   only on acceptance, so a rejected candidate can't replace it (tested in
   `tests/test_improvement_loop.py`).

**Threshold calibration** (`src/abstention.py: calibrate`).
- Candidate thresholds: the minimum observed train signal, the midpoints between consecutive
  distinct values, and the maximum + 1e-9.
- The one with the highest balanced accuracy is chosen; ties go to the smallest threshold.
- Rule: abstain iff no candidates, or signal < threshold; equality answers.

**Trade-off at the selected threshold.** Computed from the saved final-config train signals
(`artifacts/loop/run3/iter09_overlap_up/per_query.jsonl`); no new evaluation:

| Threshold | False abstentions (/140) | Failures to abstain (/28) | Balanced acc. |
|---|---:|---:|---:|
| **0.2739 (selected)** | 3 | 0 | 0.989 |
| 0.2600 | 3 | 1 | 0.971 |
| 0.2500 | 2 | 3 | 0.939 |
| 0.2470 | 1 | 3 | 0.943 |
| 0.2400 | 0 | 3 | 0.946 |

Three `unspecified_info` train negatives sit just below the threshold: `unans-026` at 0.251,
`unans-030` at 0.257 and `unans-025` at 0.271.

## 7. Iteration history

### 7.1 Runs

| Run | Spec | Change to the spec | Data used for selection | Candidates evaluated beyond baseline | Accepted chain | Evidence |
|---|---|---|---|---|---|---|
| 1 | v1 | — | train | 11 (+2 skipped: dense extra missing) | `stem_stopwords` → `doc_routing` → `doc_title_in_index` | `artifacts/loop/20261102-144050/` |
| 2, original | v2 | + `question_only_dual_abstention` | train | 12 *(session record only)* | ended at `doc_title_in_index` *(session record only)* | **directory overwritten** (§10.3) |
| 2, re-run | v3 | + `question_only_fullquery_abstention` | train | 12 (+1 skipped) | `question_only_fullquery_abstention` → `stem_stopwords` → `overlap_trim` → `overlap_up` | `artifacts/loop/run2/` |
| 3 | v3 | none | train | 12 (+1 skipped) | identical to the run-2 re-run | `artifacts/loop/run3/` |

- **Selection.** The final configuration is run 3's last accepted candidate, `overlap_up`
  (`artifacts/loop/run3/accepted_config.yaml`).
- **Counts.** Run 3 contains **12 genuine iterations beyond the baseline**: each is a distinct
  configuration with its own train evaluation. The run-2 re-run is a *re-run* of the same spec,
  not new iterations, and its identical decisions show the loop is deterministic.
- **Duration.** Each run took about 4 seconds (first and last timestamps in `iterations.jsonl`).

**Why the spec changed between runs.** Both changes were made from train diagnostics and are
recorded in the `configs/loop.yaml` change log. Adding candidates between runs is a
human-in-the-loop step outside the one-command loop.
- **v2, after run 1.** Question-only ranking more than doubled F1@5, but a single chunk-level
  abstention signal could no longer reject nonexistent-contract queries: balanced accuracy fell
  to 0.807.
- **v3, after the original run 2.** The two-threshold rule reached balanced accuracy 0.904,
  below the 0.939 guardrail. Its errors were 7 false abstentions (4 on the HPIL contract, whose
  header wording differs from the query preamble) and 4 failures to abstain, all on
  `unspecified_info` negatives *(re-checked from the identical candidate in
  `artifacts/loop/run3/iter02_question_only_dual_abstention/`)*.

### 7.2 Run 3 (selected the final configuration)

Train; `artifacts/loop/run3/iterations.jsonl` *(re-checked)*.

| # | Candidate | Hypothesis (abbreviated) | F1@5 | P@5 | R@5 | R@64 | P@1 | Bal. acc. | Decision (reason) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | baseline | reference | 0.033 | 0.019 | 0.165 | 0.462 | 0.003 | 0.982 | accepted |
| 1 | `question_only_chunk_query` | rank with the question inside the routed contract | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.807 | rejected (balanced-accuracy guardrail) |
| 2 | `question_only_dual_abstention` | same + two-threshold abstention | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.904 | rejected (balanced-accuracy guardrail) |
| 3 | `question_only_fullquery_abstention` | same ranking, full-query abstention signal | 0.077 | 0.045 | 0.439 | 0.683 | 0.097 | 0.982 | **accepted** (+0.044) |
| 4 | `stem_stopwords` | stemming + stopword removal | 0.111 | 0.066 | 0.546 | 0.701 | 0.166 | 0.989 | **accepted** (+0.035) |
| – | `hybrid_rrf` | BM25 + dense RRF | | | | | | | skipped (dense extra not installed) |
| 5 | `doc_routing` | top-1 routing with full-query ranking | 0.051 | 0.030 | 0.275 | 0.652 | 0.009 | 0.989 | rejected (−0.060) |
| 6 | `doc_title_in_index` | contract title in the indexing text | 0.109 | 0.064 | 0.539 | 0.695 | 0.164 | 0.989 | rejected (−0.003) |
| 7 | `chunk_500` | 500/75 chunks | 0.142 | 0.092 | 0.452 | 0.606 | 0.237 | 0.961 | rejected (recall@5 guardrail) |
| 8 | `overlap_trim` | trim instead of skip overlapping passages | 0.126 | 0.075 | 0.621 | 0.878 | 0.166 | 0.989 | **accepted** (+0.015) |
| 9 | `overlap_up` | overlap 300 | 0.131 | 0.079 | 0.617 | 0.878 | 0.174 | 0.989 | **accepted** (+0.004) |
| 10 | `chunk_300` | 300/45 chunks | 0.188 | 0.136 | 0.427 | 0.670 | 0.275 | 0.925 | rejected (recall@5 and balanced-accuracy guardrails) |
| 11 | `bm25_params` | k1 1.2, b 0.5 | 0.128 | 0.077 | 0.605 | 0.878 | 0.170 | 0.986 | rejected (−0.003) |
| 12 | `abstain_on_doc_signal` | document-level abstention signal | 0.131 | 0.079 | 0.617 | 0.878 | 0.174 | 0.879 | rejected (no F1 gain) |

- **Not reached.** The run stopped at `max_iterations: 12`, so `chunk_1500` and `dense_only`
  weren't reached in the v3 runs.
- **Smaller chunks.** `chunk_500` and `chunk_300` had the highest F1@5 but lost more than 0.05
  recall@5, so the predeclared guardrail rejected them; a different objective would choose
  differently.
- **Small gains.** Some accepted gains (+0.004) are within the noise of 140 queries.

### 7.3 Run 1

Train; `artifacts/loop/20261102-144050/iterations.jsonl` *(re-checked)*.

| # | Candidate | F1@5 | R@5 | P@1 | Bal. acc. | Decision |
|---|---|---|---|---|---|---|
| 0 | baseline | 0.0328 | 0.1650 | 0.0028 | 0.982 | accepted |
| 1 | `question_only_chunk_query` | 0.0766 | 0.4386 | 0.0965 | 0.807 | rejected (balanced-accuracy guardrail) |
| 2 | `stem_stopwords` | 0.0377 | 0.2136 | 0.0087 | 0.989 | accepted |
| – | `hybrid_rrf` | | | | | skipped |
| 3 | `doc_routing` | 0.0512 | 0.2748 | 0.0087 | 0.989 | accepted |
| 4 | `doc_title_in_index` | 0.0550 | 0.2930 | 0.0087 | 0.989 | accepted |
| 5–11 | `chunk_500`, `overlap_trim`, `overlap_up`, `chunk_300`, `bm25_params`, `abstain_on_doc_signal`, `chunk_1500` | 0.038–0.055 | | | 0.879–0.989 | all rejected (F1@5 not improved by ≥ 0.002) |
| – | `dense_only` | | | | | skipped |

## 8. Error analysis

**Category counts.** Train, final configuration, k = 5 (`src/diagnostics.py`;
`artifacts/error_analysis/overlap_up/summary.json`, 140 answerable queries):

| Category | Final | Baseline (`artifacts/error_analysis/baseline/summary.json`) |
|---|---:|---:|
| ok | 24 | 0 |
| wrong section (right contract, no gold overlap) | 43 | 104 |
| irrelevant extra (gold fully in top 5, precision@5 < 0.1) | 37 | 1 |
| low rank (gold in top 5, not at rank 1) | 15 | 13 |
| partial span (some gold found, recall@5 < 1) | 11 | 4 |
| chunk boundary (a short gold span cut by a passage boundary) | 7 | 13 |
| false abstention | 3 | 5 |
| wrong document / offset error | 0 / 0 | 0 / 0 |
| unanswerable: correct abstention / failure to abstain | 28 / 0 | 28 / 0 |

**Twelve illustrative failures.** They come from
`artifacts/error_analysis/overlap_up/failures.jsonl`, which holds 116 failure records; every ID,
category and metric below was *(re-checked)* against it. All are train queries under the final
configuration. Causes are hypotheses unless marked *verified*. No remediation listed here was
implemented or measured.

| ID | Contract; question | Expected evidence `[start, end)` | Actual | Category | Likely cause | Proposed remediation |
|---|---|---|---|---|---|---|
| 1 `cuad-551a572623` | BicycleTX/Crockett; exceptions to competitive restrictions | [33572, 34034] "save that nothing in this paragraph 13.2 shall prevent you…" | #1 [37817, 38817], #2 [38817, 39508] (the covenants themselves); R@5 = 0 | wrong section | lexical overlap rewards the restriction, not its carve-out | reranker; carve-out query expansion |
| 2 `cuad-0b7b50dadf` | HPIL/GINARES; expiration date | [5604, 5739] "The term of this Agreement shall be one (1) year…" | #1 [7739, 8739], insolvency boilerplate (score 2.37); R@5 = 0 | wrong section | vocabulary gap (expiration ↔ term) | dense/hybrid retrieval (implemented, not evaluated) |
| 3 `cuad-e5b265c6b3` | BicycleTX; governing law | [53956, 54252] "…the laws of England…" | inside #1 [53459, 54272]; P@5 = 0.071, R@5 = 1.0 | irrelevant extra | 296-character answer in about 4,200 returned characters | sentence-level refinement |
| 4 `cuad-cc22d5d0ab` | HPIL; governing law | [16867, 17117] | inside #1 [16376, 17340]; #2 is the table of contents [1775, 2741]; P@5 = 0.059 | irrelevant extra | table-of-contents headings match clause names | down-weight table-of-contents chunks |
| 5 `cuad-5c06b5a634` | ISA/Rubicon; exceptions to competitive restrictions | [23556, 23770] | #1 [20522, 21517], #2 [22344, 23093] (the non-compete); P@5 = 0.059 | low rank | carve-out ranked below the clause it modifies | reranker |
| 6 `cuad-92c250e51b` | Florida Chemical/Flotek; warranty duration | [3021, 3209] "FCC shall promptly, but in no event later than three (3) days…" | #1 [13245, 14220] (termination); gold via #2 [2383, 3209] | low rank | annotated text never says "warranty" | dense/hybrid retrieval |
| 7 `cuad-e568fcd380` | ISA/Rubicon; IP ownership | [14401, 14603], [14605, 15442] | #1 [13158, 14127], #2 [17453, 18445]; R@5 = 0.112 | partial span | many IP-dense sections compete | adjacent-chunk expansion; reranker |
| 8 `cuad-9d8033e4f6` | Premier Biomedical; exclusivity | [3388, 4736], [12938, 13072] | #1 [1193, 2132], a WHEREAS recital; R@5 = 0.107 | partial span | recitals repeat key terms densely | down-weight recitals |
| 9 `cuad-eb238d491d` | ISA/Rubicon; exclusivity | [5690, 6079], [6537, 7080] | #2 [6776, 7377] (start set by trimming) covers the tail of span 2; R@5 = 0.592 | chunk boundary | the trimmed remainder begins mid-clause | clause-numbering-aware splitting |
| 10 `cuad-dd123231af` | ISA/Rubicon; licenses granted | [5690, 6080], [6537, 7080] | #1 [13158, 14127], #2 [14127, 14604]; R@5 = 0.581 | chunk boundary | licence grant split and outranked | clause-aware splitting; reranker |
| 11 `cuad-2f7d42bc6c` | BicycleTX; right of first refusal/offer/negotiation | [6235, 6531], [6533, 7937] (share-option text) | abstained (0.245 < 0.2739); raw ranking R@5 = 0 | false abstention | question/gold vocabulary mismatch; possibly a loose annotation (§9) | flag the annotation |
| 12 `cuad-7646cba011` | BicycleTX; IP ownership (E1) | [44840, 45359] | abstained (0.248); raw #1 [44251, 45248] covered 408/519 gold characters | false abstention | routing and ranking correct (*verified*); the full-query normalised score is low for this long contract | better-calibrated signal on train; not a lower threshold (§6) |

**Reported cases checked during the audit** (train queries, `configs/final.yaml`):

| Case | Finding | Classification |
|---|---|---|
| E1 | = failure #12; the cause is the threshold (*verified*, §6) | genuine failure |
| E2: "What is the governing law for this contract?" | The query **names no contract**. It was previously answered from the HPIL contract by silent routing; it now abstains with `contract_not_identified` and suggestions (regression tests in `tests/test_retrieval.py`). | design defect, fixed after the test evaluations (§10.5) |
| E3: "Papa John's … and its endorser"; governing law | answered; #1 [63073, 63864] contains the Delaware clause [63649, 63806] | not a failure |
| A3: Walabot reseller; liability cap | gold [11885, 12465] covered by #1 (65 chars) + #2 (515 chars); recall@2 = 1.0 | display split across contiguous chunks |
| A4: Depomed/King; audit rights | both gold spans covered by ranks 1–3 | same as A3 |
| A7: ISA/Rubicon; renewal term | correct contract; gold [18727, 19214] at rank 1 (§9) | not a failure |
| A8: Tate & Lyle/Igene; minimum commitment | second gold span at rank 1; loose annotation (§9); `demo-check` samples a different question for this contract | annotation-consistency note |

**Demo check.** `demo-check` with `configs/final.yaml`:
- **A answerable: 4/10.** The six failures are 5 wrong-passage results and 1 false abstention
  (BicycleTX IP, i.e. E1).
- **B unanswerable: 4/4**
- **C input handling: 14/14.** An earlier version of this battery reported 13/13, but one of
  those checks passed vacuously (§11.1).

With `configs/candidate_v4.yaml` the same battery gives **A 8/10, B 4/4, C 14/14**: four of the
six failures are fixed; Theravance (rank 6) and BicycleTX IP (false abstention) remain (§11.7–11.8).
The root causes and the run-4 changes are in §11.

## 9. Limitations, risks and future work

**Observed limitations.**
- **Query-format dependence.** Routing needs a "Consider …;" preamble or an explicit contract
  choice; free-form references aren't resolved.
- **Single-contract routing.** Top-1 routing means a wrong choice gives zero recall. None
  occurred on train (140/140), where parties were named explicitly.
- **Low precision** (§5.5). Smaller chunks raised precision but failed the recall guardrail.
- **Lexical vocabulary gaps.** Expiration ↔ term and carve-outs ("save that") drive most
  wrong-section and low-rank failures.
- **Unevaluated alternatives.** Dense and hybrid retrieval are implemented but unevaluated.
- **Abstention evidence.**
  - The negative set is hand-authored, and only about 7 of its queries are realistic
    absent-information negatives.
  - Only 7 test negatives exist (§5.4).
  - The selected threshold sits close to three realistic train negatives (§6).
- **Small, homogeneous benchmark.** 29 SEC-filed contracts shared by both splits; the results
  don't establish performance on unseen contracts.
- **Gold/query consistency** (documented; no annotation was modified):
  - **A8.** The two gold spans for "minimum commitment" are a capitalisation commitment of "at
    least $21,614,000" [13653, 13922] and an annual-dividend obligation [20181, 20459]; the
    second fits loosely.
  - **Failure #11.** The gold for "right of first refusal" describes a share-option
    arrangement.
  - **A7 is not a mismatch.** CUAD file names use the SEC filer (`DUOSTECHNOLOGIESGROUP,INC_…`),
    while the contract text reads "by and between Information  System Associates, Inc." (with a
    double space in the source) and mentions Rubicon 133 times.
- **Legal-domain safety.** Results are excerpts, not interpretations. Before real legal use, the
  system would need:
  - lawyer-validated evaluation on the target contracts;
  - abstention calibrated on realistic negatives;
  - access control and audit logging.

**Future work** (proposals; none implemented or measured):
- sentence-level refinement inside top passages;
- evaluating the implemented dense/hybrid retrievers and a cross-encoder reranker;
- down-weighting recitals and table-of-contents chunks;
- clause-aware chunk boundaries;
- a length-aware abstention signal;
- an independently authored, larger negative set focused on absent-information questions;
- multi-contract retrieval for unnamed contracts;
- a single locked test evaluation.

## 10. Test-set evaluation history and protocol deviations

### 10.1 Recorded test evaluations

`artifacts/test_runs.jsonl` *(re-checked)*; the CLI refuses the test split without
`--final-test` and logs every test run:

| # | Time (IST, 2026-11-02) | Config | Fingerprint | Context |
|---|---|---|---|---|
| 1 | 14:42:30 | `provisional` (baseline settings with the train threshold) | `d64c5b4f…` | early runbook check, after loop run 1 and before any final selection |
| 2 | 15:34:05 | `overlap_up` (final) | `3254f317…` | after the final-selection commit `b4dbca3` (15:33:54) |
| 3 | 15:34:27 | `baseline` | `c41401f0…` | baseline comparison |

Runs #4–#9 (2026-11-06) are listed and discussed in §14.1.

**What run #1 revealed.** Its config is the baseline plus a key that only appeared in later code
versions, and its retrieval and abstention results equal run #3's at every k *(re-checked)*. So
it revealed only baseline test performance, and nothing about any candidate.

**No test-driven changes in the record.**
- The loop can't load test queries.
- All later changes (spec v2, v3) cite train diagnostics.
- No error-analysis or diagnostic artifact exists for the test split: all three error-analysis
  outputs are train-only (`src/cli.py: cmd_error_analysis`).
- The per-query test outputs written by `evaluate` exist only locally.

**What the record can't show.** That nobody looked at run #1's output. Three evaluations, one of
them before final selection, are weaker than a single locked final evaluation, even if no tuning
followed.

### 10.2 Negative-set chronology

| Event | Time (IST) | Evidence |
|---|---|---|
| loop run 1 starts | 14:40:50 | first timestamp in `artifacts/loop/20261102-144050/iterations.jsonl` |
| loop run 1 ends | 14:40:54 | last timestamp |
| negative set first committed | 14:44:58 | commit `20e9cf4` |

- **The commit came after the first loop run had started**, so the requirement to commit the
  frozen set before starting the loop was **not met** for run 1.
- **What is established.** Run 1's `summary.json` records SHA-256 `77d8b48ab6c6…` for the file it
  loaded, which equals the committed file and the hash in runs 2 and 3. So run 1 used exactly the
  committed content, and the content never changed.
- **What is not established.** When the file was written. That it was authored before run 1,
  without reference to system output, rests on the session record only.

### 10.3 Overwritten loop artifacts

- The original spec-v2 run used `--run-name run2`. A later spec-v3 re-run under the same name
  overwrote its directory.
- Its results survive only in the development session's console output *(session record only)*:
  12 candidates evaluated, `question_only_dual_abstention` with F1@5 0.0766 and balanced accuracy
  0.904, rejected.
- The same candidate was re-evaluated with identical code in the v3 runs and gave the same
  numbers, but no machine-readable log of the original v2 run exists.

### 10.4 Per-query outputs not in version control

`.gitignore` excludes `artifacts/**/per_query*.jsonl`. Aggregate metrics, configs, loop logs and
train failure records are committed. The per-query outputs behind the reported metrics exist only
in the author's working tree.

### 10.5 Change after the test evaluations

- **What changed.** After runs #2/#3, `query.require_contract: true` was added to
  `configs/final.yaml` (commit `0e4abd3`).
- **Why the test results are unaffected.**
  - The flag can only turn "answered" into "abstained", and only for queries without a preamble.
  - All 194 benchmark queries have a preamble (checked from query text), so no answerable result
    can change.
  - All 7 test negatives were already abstained.

  The reported test metrics therefore also hold for the current configuration. No fourth test
  evaluation was made.
- **Train check.** The train evaluation in `artifacts/eval/overlap_up_train_20261102-162333/`
  reproduces run 3's iteration 9 exactly.
- **Fingerprints.** The current `configs/final.yaml` fingerprint is `72c8f8c97f8f7ab1`. Removing
  the new key gives `3254f317b4c41e2c`, the tested configuration.

Loop run 4 and `configs/candidate_v4.yaml` (§11) were also produced after the test evaluations,
on train only. Unlike `require_contract`, they change ranking for benchmark queries, so the
test results of runs #2/#3 do **not** apply to `candidate_v4`; its own test result is run #5
(§14).

### 10.6 Provenance

| Item | Value |
|---|---|
| tested final config fingerprint | `3254f317b4c41e2c` (= `artifacts/loop/run3/accepted_config.yaml`) |
| current `configs/final.yaml` fingerprint | `72c8f8c97f8f7ab1` (tested config + `require_contract: true`) |
| final-config index fingerprint | `8d4a7984b2102b7b` (2,027 chunks) |
| final-selection commit | `b4dbca3`; post-test audit commit `0e4abd3` |
| `cuad.json` / manifest / negative set SHA-256 | `8e0405b15fb8…` / `204a4d7efb3a…` / `77d8b48ab6c6…` |

Config fingerprints are SHA-256 hashes of the resolved config (defaults merged), excluding `name`
and `status`. They are comparable only within one code version.

**Reproducibility.** The system is deterministic: no sampling, and tie-breaking is explicit.
Commands are in README.md §Reproduction runbook. A clean spec-v3 run should reproduce
`artifacts/loop/run3/`. Two historical items can't be reproduced as artifacts: the original v2
run (§10.3) and the uncommitted per-query outputs (§10.4).

## 11. Post-test, train-only improvement: run 4 (spec v4)

All work in this section used **train data only**. No test evaluation was run:
`artifacts/test_runs.jsonl` still has 3 records. The gold annotations, split and frozen negative
set were not changed; the negative set's SHA-256 recorded by run 4 is `77d8b48ab6c6…`, the same as
before.

### 11.1 Document-filter demo check: a vacuous pass

- **The old check.** It used `sorted(documents)[0]`, the ALCO Stores agency agreement, with
  "What is the governing law for this contract?".
- **What happened.** That contract never contains "govern" or "law". Retrieval found one weak
  passage (signal 0.125 < 0.2739), and the system correctly abstained.
- **Why it passed anyway.** The check `all(passage in doc)` is true for an empty list.
- **Diagnosis.** The filter itself was correct; the fixture was meaningless.
- **Fix** (`src/demo_check.py`):
  - The check now uses a known answerable train pair: the first train governing-law query and
    its gold contract.
  - It requires at least one passage, all from that contract, and an overlap with gold.
  - A second check confirms that a document filter overrides a different contract named in the
    query.
- **New regression tests** (`tests/test_retrieval.py`, `tests/test_end_to_end.py`):
  - an alias and the full ID give identical, non-empty results;
  - an invalid ID raises an error;
  - a contract with no relevant passages returns nothing from other contracts;
  - a filter overrides the contract named in the query;
  - real-data check: `PapaJohns` with the governing-law question returns the Delaware clause.

### 11.2 Root causes of the six failing answerable demo queries (train, `configs/final.yaml`)

All six were routed to the **correct contract**, so none is a routing failure.

| Query | First gold rank (of 64) | Root cause | Category |
|---|---|---|---|
| `cuad-0f789ebcf3` Bon-Ton, anti-assignment | 15 | in this bankruptcy agency agreement "assign" (of leases) appears everywhere; the gold clause is "may not be assigned … without the prior written consent" | BM25 ranking + vocabulary |
| `cuad-05251665f3` Sucampo, audit rights | not retrieved | the gold text grants "reasonable access … to books and records" and never says "audit" | lexical vocabulary mismatch |
| `cuad-3fdb534e55` Tate & Lyle, exceptions to competitive restrictions | 6 | the gold uses "Except as set forth … nothing … shall prevent … engaging"; a near miss | BM25 ranking + vocabulary |
| `cuad-51b4e44436` Theravance, termination for convenience | 10 | the gold says "sole and absolute discretion … at any time", not "convenience" | lexical vocabulary mismatch |
| `cuad-5fce387d80` Depomed/King, exclusivity | 8 | after stopwords the query is `exclus` + `agreement`; the generic "agreement" ranks "This Agreement will be construed…" boilerplate first | BM25 ranking (generic template term) |
| `cuad-7646cba011` BicycleTX, IP ownership | 1 (408/519 gold characters) | retrieval is correct; the full-query signal (0.248) is normalised by preamble + question terms although no single chunk matches both (header vs clause) | score normalisation / abstention threshold |

None of the six was a chunk-boundary failure.

### 11.3 Changes

All are configuration options that default to off, so existing configurations are unchanged.
Run 4's baseline iteration reproduced `configs/final.yaml`'s train metrics exactly.

| Option | Implementation | Effect |
|---|---|---|
| `query.drop_generic_terms` | `src/text.py: GENERIC_LEGAL_TERMS` (contract, agreement, clause, provision, include, hereunder, …) removed from the **ranking** query | ranking only |
| `query.expand`, `query.expansion_weight` | `src/expansion.py`: 29 concept-keyed rules (e.g. audit → inspect, books, records, access) triggered by the question text; expansion terms weigh 0.5 (typed terms 1.0) in a weighted BM25 (`BM25.scores(weights=…)`) | ranking only |
| `retrieval.refine` | shrink each passage to its best ≤ `max_chars` sentence window (exact offsets) | passages |
| `abstention.signal: chunk_split_bm25_norm` | preamble and question matches normalised separately | abstention |

Abstention signals are always computed from the unmodified query, so generic-term removal and
expansion can't change them. They change abstention only when the ranking query has no matching
chunk at all, which returns no candidates (this explains the 5 false abstentions in iteration 1).

### 11.4 Experiments

Run 4: `python -m src.cli improve --config configs/final.yaml --spec configs/loop_v4.yaml --run-name run4_v4`.
- **Spec:** [`configs/loop_v4.yaml`](configs/loop_v4.yaml), with the same acceptance rule as §6.
- **Log:** `artifacts/loop/run4_v4/iterations.jsonl`.
- **Data:** train, n = 140 answerable / 28 unanswerable.
- **Demo:** `demo-check` was run afterwards on each iteration's `config_used.yaml`, for diagnosis
  only.

| # | Candidate (one change) | P@1 | R@1 | P@5 | R@5 | F1@5 | R@64 | False abst. | Bal. acc. | Demo A / B / C | Decision (reason) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | baseline = `configs/final.yaml` | 0.1745 | 0.4032 | 0.0787 | 0.6174 | 0.1306 | 0.8778 | 3/140 | 0.989 | 4/10 · 4/4 · 14/14 | reference |
| 1 | `v4_drop_generic_terms` | 0.1757 | 0.4064 | 0.0917 | 0.6648 | 0.1507 | 0.8383 | 5/140 | 0.982 | 7/10 · 4/4 · 14/14 | **accepted** (+0.0202) |
| 2 | `v4_refine_600` | 0.2753 | 0.1975 | 0.1137 | 0.3396 | 0.1528 | 0.4582 | 5/140 | 0.982 | 5/10 · 4/4 · 13/14 | rejected (recall@5 guardrail) |
| 3 | `v4_refine_400` | 0.2246 | 0.1519 | 0.1097 | 0.2867 | 0.1367 | 0.3937 | 5/140 | 0.982 | 4/10 · 4/4 · 13/14 | rejected (F1@5 −0.0141) |
| 4 | `v4_chunk_600` (600/120) | 0.2100 | 0.3303 | 0.1185 | 0.6000 | 0.1819 | 0.7868 | 12/140 | 0.939 | 5/10 · 3/4 · 14/14 | rejected (recall@5 guardrail) |
| 5 | `v4_query_expansion` (weight 0.5) | 0.2464 | 0.5508 | 0.1049 | 0.8095 | 0.1743 | 0.9517 | 3/140 | 0.989 | 8/10 · 4/4 · 14/14 | **accepted** (+0.0236) |
| 6 | `v4_expansion_weight_0_3` | 0.2380 | 0.5331 | 0.1035 | 0.7918 | 0.1717 | 0.9517 | 3/140 | 0.989 | 8/10 · 4/4 · 14/14 | rejected (F1@5 −0.0026) |
| 7 | `v4_split_abstention_signal` | 0.2464 | 0.5508 | 0.1049 | 0.8095 | 0.1743 | 0.9517 | 4/140 | 0.986 | 8/10 · 4/4 · 14/14 | rejected (no F1 change; abstention also worse) |

Correct abstention was 28/28 in every iteration except `v4_chunk_600` (27/28), and offset errors
were 0 throughout. The accepted configuration is iteration 5, saved as
[`configs/candidate_v4.yaml`](configs/candidate_v4.yaml) (`name: candidate_v4`,
`status: candidate`). Its train evaluation with the stored threshold reproduces these numbers
(`artifacts/eval/candidate_v4_train_20261102-171852/`).

### 11.5 Before vs after (train, n = 140 answerable / 28 unanswerable)

| Metric | `configs/final.yaml` | `configs/candidate_v4.yaml` |
|---|---:|---:|
| precision@1 | 0.1745 | 0.2464 |
| recall@1 | 0.4032 | 0.5508 |
| precision@5 | 0.0787 | 0.1049 |
| recall@5 | 0.6174 | 0.8095 |
| F1@5 | 0.1306 | 0.1743 |
| recall@64 | 0.8778 | 0.9517 |
| false abstentions | 3/140 | 3/140 |
| correct abstentions | 28/28 | 28/28 |
| balanced abstention accuracy | 0.989 | 0.989 |
| offset errors | 0 | 0 |
| demo A / B / C | 4/10 · 4/4 · 14/14 | 8/10 · 4/4 · 14/14 |

- **Still failing in the demo:**
  - Theravance (termination for convenience): the gold clause moved from rank 10 to 6, still
    outside the top 5.
  - BicycleTX IP (E1): still a false abstention; lexical signals can't separate it from its
    unanswerable counterpart (§11.8).
- **Regressions:**
  - Recall@64 fell in iteration 1 (0.878 → 0.838) and recovered with expansion (0.952).
  - Iteration 1 alone caused 2 extra no-candidate abstentions; expansion removed them.

### 11.6 Caveats on these results

- **In-sample gain.** The expansion rules were written after inspecting train failures,
  including the gold text of the six demo queries; for example, audit → books/records/access, and
  convenience → at any time/discretion. The gain is therefore an in-sample (train) estimate.
- **Gain on queries that didn't inform the rules.** Recomputed from the saved per-query files on
  the 130 train queries outside the demo set: F1@5 rose from 0.1338 to 0.1733 and recall@5 from
  0.6281 to 0.8087. That is similar to the full-train gain, so the improvement isn't confined to
  the inspected queries. It is still train data.
- **Possible template coupling.** CUAD question templates are shared between train and test, so
  concept-keyed rules may transfer, but this is **unmeasured**. Evaluating `candidate_v4` on test
  would be test evaluation #4, after the earlier result on the same split had already been seen.
  It wasn't done; whether to do it is the author's decision.
- **Rejected candidates.** Passage refinement and smaller chunks raised precision but cut recall
  far beyond the guardrail.
- **Protocol limitation.** The split abstention signal couldn't be accepted under an F1-only
  primary metric, and on its own merits it was slightly worse (4/140 false abstentions). The
  primary metric doesn't reward changes that affect only abstention.

**Reproduce:**
```bash
python -m src.cli improve --config configs/final.yaml --spec configs/loop_v4.yaml --run-name <new-name>
python -m src.cli evaluate --config configs/candidate_v4.yaml --no-calibrate
python -m src.cli demo-check --config configs/candidate_v4.yaml
# single-change ablation (§11.7); use new --out names
python -m src.cli evaluate --config configs/experiments/exp1_drop_generic.yaml --out artifacts/eval/<new>_B
python -m src.cli evaluate --config configs/experiments/exp2_expansion.yaml --out artifacts/eval/<new>_C
python -m src.cli evaluate --config configs/experiments/exp3_drop_generic_expansion.yaml --out artifacts/eval/<new>_D
```

### 11.7 Single-change ablation (train)

To separate the two accepted changes, each was evaluated **alone** against the reference under
identical settings: train split, n = 140 answerable / 28 unanswerable, abstention threshold
calibrated on train per configuration, which selected 0.2739 in all four cases.
- Configs: `configs/experiments/`
- Outputs: `artifacts/eval/exp_{A,B,C,D}_train/`
- Experiment 0 re-ran `candidate_v4` and reproduced iteration 5 of run 4 exactly
  (`artifacts/eval/exp0_reproduce_candidate_v4_train/`), and again after the later code changes
  (`exp0b_candidate_v4_after_code_change/`).

| Config | k | 1 | 2 | 4 | 5 | 8 | 16 |
|---|---|---|---|---|---|---|---|
| A: `configs/final.yaml` | P | 0.1745 | 0.1246 | 0.0881 | 0.0787 | 0.0614 | 0.0457 |
| | R | 0.4032 | 0.4740 | 0.5729 | 0.6174 | 0.6736 | 0.7806 |
| | F1 | 0.2228 | 0.1818 | 0.1416 | 0.1306 | 0.1073 | 0.0835 |
| B: generic-term removal only | P | 0.1757 | 0.1406 | 0.1035 | 0.0917 | 0.0709 | 0.0561 |
| | R | 0.4064 | 0.5192 | 0.6482 | 0.6648 | 0.7155 | 0.8043 |
| | F1 | 0.2242 | 0.2049 | 0.1662 | 0.1507 | 0.1224 | 0.0999 |
| C: expansion only (weight 0.5) | P | 0.2266 | 0.1641 | 0.1093 | 0.0941 | 0.0701 | 0.0442 |
| | R | 0.5024 | 0.5880 | 0.7220 | 0.7471 | 0.8219 | 0.8973 |
| | F1 | 0.2836 | 0.2358 | 0.1769 | 0.1567 | 0.1235 | 0.0820 |
| **D: both (= `candidate_v4`)** | P | 0.2464 | 0.1827 | 0.1210 | 0.1049 | 0.0757 | 0.0476 |
| | R | 0.5508 | 0.6524 | 0.7868 | 0.8095 | 0.8651 | 0.9186 |
| | F1 | 0.3108 | 0.2636 | 0.1958 | 0.1743 | 0.1332 | 0.0877 |

| Config | False abstentions | Correct abstentions | Failure to abstain | Bal. acc. | Offset errors |
|---|---:|---:|---:|---:|---:|
| A | 3/140 | 28/28 | 0.000 | 0.989 | 0 |
| B | 5/140 | 28/28 | 0.000 | 0.982 | 0 |
| C | 3/140 | 28/28 | 0.000 | 0.989 | 0 |
| D | 3/140 | 28/28 | 0.000 | 0.989 | 0 |

**Reading the ablation.**
- **D wins.** It is best at every k, except that B has a higher P@16 (0.0561 vs 0.0476).
- **C beats B.** Expansion alone outperforms generic-term removal alone.
- **B's extra false abstentions.** With generic words removed, some questions keep no word that
  matches any chunk; expansion removes these cases in D.

**Per-failure effect.** Rank of the first gold-overlapping passage for each of the six audited
train queries; "abst." means the query is abstained:

| Query | A | B | C | D |
|---|---|---|---|---|
| Bon-Ton, anti-assignment | 15 | **1** | 8 | **1** |
| Sucampo, audit rights | not in top 64 | not in top 64 | **1** | **1** |
| Tate & Lyle, exceptions to competitive restrictions | 6 | **4** | **1** | **1** |
| Depomed/King, exclusivity | 8 | **1** | **4** | **1** |
| Theravance, termination for convenience | 10 | 10 | 7 | 6 |
| BicycleTX, IP ownership | 1 (abst.) | 1 (abst.) | 1 (abst.) | 1 (abst.) |

- **Sucampo** is fixed only by expansion; its gold text uses books, records and access instead of
  "audit".
- **Bon-Ton and Depomed** are fixed mainly by removing generic template terms.
- **Theravance (remaining miss).** The gold chunk is in the candidate pool at rank 6, but the top
  competitor covers more ranking terms (6 vs 5), so a term-coverage reranker wouldn't promote it.
  The source text is also damaged inside the gold span (`"l ieu of  not ice"`), so "notice" can't
  match. No reranker was implemented.

### 11.8 BicycleTX false abstention (E1) and experiment 4

**Rule tested.** Experiment 4 tested a two-part rule, `abstention.signal: identity_and_question`
(`configs/experiments/exp4_identity_question_abstention.yaml`). It abstains if contract identity
is not confirmed (`preamble_bm25_norm` < `doc_threshold`) **or** the question-only answerability
score (`chunk_bm25_norm`) is below `threshold`, with both thresholds jointly calibrated on train.

**Result:**
- false abstentions rose to **17/140** (from 3);
- one negative was answered (27/28 correct abstentions);
- balanced accuracy fell to **0.921** (from 0.989).

It is **rejected** (`artifacts/eval/exp_E4_train/`).

**Root cause.** The answerable IP question and its unanswerable counterpart `unans-025` (the same
BicycleTX contract, asking for Nigel Crockett's passport number and date of birth) can't be
separated lexically:

| Query | full-query signal | question-only signal | identity signal |
|---|---:|---:|---:|
| E1 IP question (answerable) | 0.2485 | 0.2033 | 0.3782 |
| `unans-025` passport question (unanswerable) | 0.2708 | 0.3131 | 0.3782 |

The unanswerable query scores **higher** on both answer signals, so any threshold low enough to
answer E1 also answers `unans-025`. The calibrated threshold (0.2739) keeps the better overall
train trade-off (§6). This is a limit of lexical evidence, not a calibration bug. Fixing it would
need a model of answer type or meaning; nothing like that was tested.

The case is recorded as `tests/test_end_to_end.py::test_real_bicycletx_ip_is_answered`, marked
`xfail(strict=True)`, so a future fix shows up as an XPASS failure instead of passing silently.

### 11.9 Further rejected experiment and acceptance log

**Experiment 5.** `query.expansion_skip_function_words: true` (on top of D) stops function words
such as "any", from the phrase "at any time", from being added as expansion terms. F1@5 was
unchanged at 0.1743 (R@16 0.9186 → 0.9238), below the +0.002 acceptance threshold, so it was
**rejected**. The option stays available, default off (`artifacts/eval/exp_E5_train/`).

| Experiment | Change vs reference | Train F1@5 | Train R@5 | False abst. | Decision |
|---|---|---:|---:|---:|---|
| A | none (`configs/final.yaml`) | 0.1306 | 0.6174 | 3/140 | reference |
| B | generic-term removal | 0.1507 | 0.6648 | 5/140 | superseded by D |
| C | concept expansion | 0.1567 | 0.7471 | 3/140 | superseded by D |
| **D** | **B + C (`candidate_v4`)** | **0.1743** | **0.8095** | **3/140** | **accepted** |
| 4 | `identity_and_question` abstention (on A) | 0.1306 | 0.6174 | 17/140 | rejected |
| 5 | D + skip expansion function words | 0.1743 | 0.8095 | 3/140 | rejected (no gain) |

**Tests.** `python -m pytest -q` gives **101 passed, 1 xfailed**; the expected failure is the
BicycleTX case above. Regression tests cover:
- the recorded expansion terms and weights;
- the user's question is never rewritten;
- routing is unaffected by query refinement;
- generic-term removal never drops negation or exception words;
- the identity-and-question rule;
- real-data checks that the four fixed train cases stay in the top 5 with exact offsets.

**Remaining limitations.**
- **Train-only gain.** All gains here are train-only (§11.6).
- **Two unresolved failures.** Theravance and BicycleTX remain.
- **Negation.** The global stopword list (unchanged since the baseline) removes "no", "not" and
  "nor" from search text.
- **Untested alternatives.** Dense/hybrid retrieval and reranking remain unevaluated.
  *(Update: cross-encoder reranking was evaluated afterwards on train and rejected; see §12.
  Dense/hybrid retrieval remains unevaluated.)*

## 12. Train-only experiment 6: cross-encoder reranking (rejected)

This section was written after the implementation and the train runs below were complete. All
numbers are train-split measurements (140 answerable / 28 unanswerable). **No test-split
evaluation was run** (`artifacts/test_runs.jsonl` still has 3 entries). `configs/final.yaml` and
`configs/candidate_v4.yaml` were not modified.

### 12.1 Motivation

After run 4, some relevant clauses were still ranked below lexically closer but irrelevant ones,
mainly Theravance (§11.7: gold at rank 6 because "termination for convenience" is written
"in its sole and absolute discretion … at any time"). A cross-encoder reads the question and a
passage together, so it can in principle match meaning rather than shared words. The experiment
asks whether it ranks BM25's own candidates better. BM25 stays the first-stage retriever.

### 12.2 Two-stage architecture (`src/rerank.py`, `src/retrieval.py: Index.retrieve`)

```
query ─► parse preamble / question ─► route to one contract (or --document filter)
      ─► abstention signals from BM25 (unchanged, computed here, before any reranking)
      ─► ranking query: generic-term removal + concept expansion (unchanged)
      ─► BM25 ranks the routed contract's chunks (stage 1, unchanged)
      ─► NEW, only if reranker.enabled: cross-encoder scores (question, chunk text) for the top
         candidate_k BM25 chunks; those are re-sorted by that score, the rest keep BM25 order
      ─► overlap handling (trim) and top-k selection (unchanged) ─► abstention decision (unchanged)
```

- **Integration point.** Between the BM25-sorted chunk list and `_select`. Reranking works on
  whole chunks, before the overlap policy trims passages, so trimming still runs in the final
  order and returned passages never overlap.
- **What can change.** Only the order. Reranking never adds or removes candidates, so routing and
  the document filter hold. Chunk ids, document ids, offsets and text are untouched, and
  `Pipeline.search` still checks every passage against the source.
- **Scores.** `Passage.score` remains the BM25 score. Reranked passages also carry `rerank_score`
  and `bm25_rank` (the chunk's 1-based BM25 rank). Both fields are omitted when reranking is off,
  so disabled output is byte-identical to before.
- **Ties** on the reranker score keep BM25 order. Duplicate chunk ids are scored once. An empty
  candidate list never loads or calls the model.
- **Failures.** A model-load or inference failure, a wrong number of scores, or NaN scores raise
  `RerankError`, which `Pipeline` re-raises as `PipelineError`. There is no silent fallback to
  BM25 order.
- **Lazy loading.** The model loads on the first query that has candidates, never at import or
  when the index is built.
- **Query text.** `reranker.query_text: question` passes the question without the contract
  preamble, the same text BM25 ranks with. Routing has already chosen the contract.

Configuration (defaults in `src/config.py`; `enabled: false` everywhere except the exp 6 files):

```yaml
reranker:
  enabled: false
  backend: cross_encoder
  model_name: cross-encoder/ms-marco-MiniLM-L-6-v2
  candidate_k: 50        # BM25 chunks re-scored; the final count is still top_k / max_k
  batch_size: 16
  device: cpu
  max_length: 512        # tokens per (question, chunk) pair
  query_text: question   # question | full
  local_files_only: false  # true => offline after the first download
```

- **Fingerprints.** A disabled reranker section is excluded from `config_fingerprint`, so adding
  the defaults did not change the fingerprints of existing configs (`configs/final.yaml` is still
  `e1c913daee266b6c` in this code version). The index fingerprint is unchanged
  (`8d4a7984b2102b7b`), because reranking doesn't change the index.
- **Abstention signal.** A new signal `rerank_top_score` (the best reranker score) was added for
  a possible separate abstention experiment. It requires `reranker.enabled` and is not used by
  any evaluated config (§12.6).

### 12.3 Model

| Item | Value |
|---|---|
| Model | `cross-encoder/ms-marco-MiniLM-L-6-v2` (Hugging Face Hub, revision `233902d…`) |
| Training data | MS MARCO passage ranking (web search queries); **not legal text** |
| Size | 22,713,601 parameters (measured); `model.safetensors` 87 MB on disk |
| Licence | Apache-2.0 (model card). It was trained on MS MARCO, whose own terms restrict use to non-commercial research; check both before any commercial use |
| Dependencies | optional extra `uv sync --extra dense` (sentence-transformers 6.2.0, CPU-only torch 2.15.0) |
| Download | once, from the Hub, on first use; afterwards `local_files_only: true` or `HF_HUB_OFFLINE=1` runs offline |
| Hardware | CPU only (measured on 12 logical CPUs, 15 GiB RAM); no GPU, no paid API |

Why this model: it is the smallest widely used general-purpose cross-encoder, runs on CPU and
is already supported by the project's optional dependency stack. It was **not** chosen for legal
competence. Whether a web-search relevance model transfers to contract clauses was the open
question, and only this one model was evaluated. No other models were downloaded.

### 12.4 Train results

Commands (each run in a new directory; thresholds calibrated on train for each config, as in
§11.7):

```bash
python -m src.cli validate-data
python -m src.cli evaluate --config configs/final.yaml --split train --out artifacts/eval/exp6_A_final_train
python -m src.cli evaluate --config configs/candidate_v4.yaml --split train --out artifacts/eval/exp6_B_candidate_v4_train
python -m src.cli evaluate --config configs/experiments/exp6_cross_encoder.yaml --split train --out artifacts/eval/exp6_C_cross_encoder_train
python -m src.cli evaluate --config configs/experiments/exp6b_cross_encoder_k10.yaml --split train --out artifacts/eval/exp6b_cross_encoder_k10_train
python -m src.cli compare artifacts/eval/exp6_A_final_train artifacts/eval/exp6_B_candidate_v4_train \
  artifacts/eval/exp6_C_cross_encoder_train artifacts/eval/exp6b_cross_encoder_k10_train \
  --qids cuad-51b4e44436 cuad-0f789ebcf3 cuad-05251665f3 cuad-3fdb534e55 cuad-5fce387d80 cuad-7646cba011
```

A and B reproduce §11.7 exactly, which confirms that the code change left the reranker-off path
unchanged. Exp 6b (`candidate_k: 10`) is a single sensitivity check. It was not tuned further,
and it is not a selection candidate.

| Metric | A: `final.yaml` | B: `candidate_v4` | C: B + rerank top 50 | 6b: B + rerank top 10 |
|---|---:|---:|---:|---:|
| precision@1 | 0.1745 | **0.2464** | 0.1874 | 0.1991 |
| recall@1 | 0.4032 | **0.5508** | 0.4259 | 0.4430 |
| F1@1 | 0.2228 | **0.3108** | 0.2371 | 0.2471 |
| precision@2 | 0.1246 | **0.1827** | 0.1370 | — |
| recall@2 | 0.4740 | **0.6524** | 0.5463 | — |
| F1@2 | 0.1818 | **0.2636** | 0.2016 | — |
| precision@5 | 0.0787 | **0.1049** | 0.0841 | 0.0923 |
| recall@5 | 0.6174 | **0.8095** | 0.7050 | 0.7514 |
| F1@5 | 0.1306 | **0.1743** | 0.1419 | 0.1553 |
| recall@10 † | 0.7039 | **0.8805** | 0.8248 | **0.8805** |
| recall@64 | 0.8778 | 0.9517 | 0.9517 | 0.9517 |
| false abstentions | 3/140 | 3/140 | 3/140 | 3/140 |
| correct abstentions | 28/28 | 28/28 | 28/28 | 28/28 |
| failure to abstain | 0/28 | 0/28 | 0/28 | 0/28 |
| balanced accuracy | 0.989 | 0.989 | 0.989 | 0.989 |
| calibrated threshold | 0.2739 | 0.2739 | 0.2739 | 0.2739 |
| offset errors | 0 | 0 | 0 | 0 |
| demo A / B / C | 4/10 · 4/4 · 14/14 | 8/10 · 4/4 · 14/14 | 6/10 · 4/4 · 14/14 | not run |

† Recall@10 is not in `evaluation.k_values`. `compare` recomputes it with `src/metrics.py` from
the stored top-10 passages, and it checks that the same recomputation reproduces `metrics.json` at
k = 5 for every run. Exp 6b's k = 2 values are in its `metrics.json`; they were omitted here
because exp 6b is only a sensitivity check. Recall@10 is identical for B and 6b because
reranking the top 10 only permutes them.

**Reading.** With the top-50 pool (C), every retrieval metric is worse than `candidate_v4` at
every reported k ≤ 10. With the top-10 pool (6b), every metric is worse at k ≤ 5, and recall@10
is equal. At k = 64 recall is unchanged by construction, because the same candidates are returned
in a different order. The shallower pool hurts less only because it moves fewer passages. Against
the BM25 order the top-1 passage changed for 91/168 queries with top 50 and 89/168 with top 10.
In the inspected cases the move was usually away from gold, consistent with the metric drops.

**Abstention.** Unchanged: 0 of 168 decisions differ between B and C. This is expected, because
the configured signal (`chunk_full_bm25_norm`) is the best BM25 score over the routed contract's
chunks. It is computed before reranking and doesn't depend on which passage ends up at rank 1.
Reranking therefore cannot change which evidence abstention sees.

### 12.5 The six audited cases (rank of the first gold-overlapping passage)

From `artifacts/eval/exp6_comparison_k10_train.json`; "bm25" is that chunk's stage-1 rank and
"ce" its reranker logit:

| Query | B: `candidate_v4` | C: rerank top 50 | 6b: rerank top 10 |
|---|---|---|---|
| Theravance, termination for convenience (`cuad-51b4e44436`) | 6 | 10 (bm25 6, ce −6.68) | 7 |
| Bon-Ton, anti-assignment (`cuad-0f789ebcf3`) | 1 | 9 (bm25 2, ce −5.46) | 5 |
| Sucampo, audit rights (`cuad-05251665f3`) | 1 | 6 (bm25 1, ce −7.32) | 3 |
| Tate & Lyle, exceptions to competition (`cuad-3fdb534e55`) | 1 | 5 (bm25 4, ce −6.75) | 2 |
| Depomed/King, exclusivity (`cuad-5fce387d80`) | 1 | 4 (bm25 1, ce −8.02) | 2 |
| BicycleTX, IP ownership (`cuad-7646cba011`) | 1, abstained | 2, abstained | 2, abstained |

- **Theravance is not fixed.** It falls from rank 6 to 10. The model's top choice for this query
  was a misrepresentation/entire-agreement clause that BM25 ranked 21st (ce −3.23 vs −6.68 for
  gold). Gold texts score strongly negative in all five answerable cases, so the model does not
  recognise these clauses as answers.
- **Bon-Ton, Sucampo, Tate & Lyle and Depomed** were all at rank 1 under `candidate_v4`, and
  reranking pushes each of them down.
- **BicycleTX (E1) is still a false abstention.** Reranking can't change that decision (§12.4).
  As a separate offline check, the reranker's best score was compared for E1 and its unanswerable
  counterpart `unans-025` (§11.8): −2.28 for E1 vs −1.29 for `unans-025`. As with the lexical
  signals, the unanswerable query scores **higher**, so this signal can't separate the pair
  either.

### 12.6 Reranker-based abstention: not warranted

No separate abstention run was made. Instead, the existing `calibrate()` was applied to the best
reranker score of the exp 6 train queries (from `per_query.jsonl`; 140 answerable, and 13 of the
28 negatives that have candidates; the other 15 have no candidates and always abstain). The best
threshold (−5.39) gives balanced accuracy **0.760** on those queries: 116/140 answered and 9/13
abstained. Including the 15 no-candidate negatives, that is about 0.84 overall, versus **0.989**
for the BM25 signal. The `rerank_top_score` signal stays available in code (default unused,
covered by tests), but no config uses it.

### 12.7 Operational measurements (one process per run, this machine)

From `metrics.json → operational` (`src/evaluation.py: operational_metrics`):

| Measurement | B: `candidate_v4` | C: rerank top 50 | 6b: rerank top 10 |
|---|---:|---:|---:|
| index build (chunk + BM25) | 0.39 s | 0.40 s | 0.42 s |
| model load (warm cache) | — | 6.3 s | 7.0 s |
| mean candidates reranked per query | — | 29.9 | 9.5 |
| mean reranking latency per reranked query | — | 1.12 s | 0.32 s |
| mean total query latency (all 168 queries) | 0.0008 s | 1.02 s | 0.29 s |
| peak resident memory (process) | 55 MiB | 945 MiB | 862 MiB |

- **Model load** is the first `CrossEncoder(...)` call with the files already cached, including
  the Hub freshness check (`local_files_only: false`). The very first download wasn't cleanly
  timed.
- **Mean query latency** includes queries that never reach the reranker (no candidates), so it
  can be below the mean reranking latency.
- **Peak memory** is the process's `ru_maxrss`, so it includes importing torch.
- **Cost.** Reranking adds about 1,300× query latency at `candidate_k: 50`, roughly 17× memory,
  and a torch dependency.

### 12.8 Limitations of this experiment

- **One model.** A single general-domain model was evaluated. A cross-encoder trained or
  fine-tuned on legal or contract data might behave differently. That is unmeasured, and
  fine-tuning on this benchmark's train split would need care to avoid in-sample gains.
- **Untested settings.** Pure reranking replaces the BM25 order inside the pool. Score fusion
  (e.g. RRF of BM25 and reranker ranks) was not tried.
- **Chunk text only.** The model scores the whole chunk (≤ 1,000 characters), not the trimmed
  passage that is returned.
- **Train only, in-sample.** Results are from the train split. The six cases also informed
  `candidate_v4`'s expansion rules (§11.6), so B's numbers on them are in-sample.
- **Determinism.** CPU inference repeated within this environment, but the results haven't been
  checked across torch versions or hardware.

### 12.9 Decision

**Rejected; reranking stays experimental and off.** On train, the cross-encoder lowers P@1 from
0.2464 to 0.1874, R@5 from 0.8095 to 0.7050 and F1@5 from 0.1743 to 0.1419. It fixes none of the
audited failures, demotes the four fixed ones, and leaves abstention unchanged. It also costs
about a second per query and about 0.9 GiB of memory. `configs/candidate_v4.yaml` remains the
best train configuration, and `configs/final.yaml` remains the tested one. The code path is kept,
off by default and covered by tests, so that a legal-domain reranker can be evaluated later
under the same protocol.

**Tests.** `python -m pytest -q` gives **130 passed, 1 xfailed** (29 new tests in
`tests/test_rerank.py`, using mocked scorers plus one optional real-model smoke test). The xfail
is still the BicycleTX case.

## 13. Train-only investigation: why reranking regressed, alternative rerankers, evidence verification

Written after all runs below completed. Train split only (140 answerable / 28 unanswerable).
**No test-split evaluation was run** (`artifacts/test_runs.jsonl` still has 3 entries).
`configs/final.yaml` and `configs/candidate_v4.yaml` were not modified, and no configuration was
promoted. Labels used below: **[measured]** = from an artifact; **[hypothesis]** = not
measured; **[post-hoc]** = designed after the relevant train results were seen.

### 13.1 Why the demo check fell from 8/10 to 6/10 with the MiniLM reranker [measured]

Diagnostics re-ran the 10 answerable and 4 unanswerable demo queries, capturing the full BM25
chunk order and every cross-encoder (CE) score. No code was changed for this.

| Demo query (question type) | Gold chunk BM25 rank | Gold CE score | Gold rank after rerank | Demo B → C |
|---|---|---|---|---|
| expiration date | 1, 2 | 1.43 | 1 | pass → pass |
| governing law | 1 | 0.70 | 1 | pass → pass |
| cap on liability | 1, 2 | −3.63 | 1 | pass → pass |
| **Bon-Ton, anti-assignment** | 1, 2 | −5.53, −5.46 | 10, 9 | **pass → FAIL** |
| licences granted | 1, 2 | −4.67, −0.65 | 4, 1 | pass → pass |
| **Sucampo, audit rights** | 1, 2, 9 | −7.32 | 6 | **pass → FAIL** |
| Tate & Lyle, exceptions to competition | 1, 4 | −8.40, −6.75 | 12, 5 | pass → pass (only via its rank-4 chunk) |
| Theravance, termination for convenience | 6, 8 | −6.68 | 10 | fail → fail |
| Depomed, exclusivity | 1 | −8.02 | 4 | pass → pass |
| BicycleTX, IP ownership | 1, 6 | −5.05, −3.98 | 5, 2 | fail (abstained) → fail (abstained) |

- **Cause.** The two new failures are pure ranking regressions. In both, the gold chunk was BM25
  rank 1–2 and in the pool, and the CE moved it to rank 6–10. Top-k selection only takes the new
  top 5; the selection code is not at fault. The unanswerable demo queries stay abstained,
  because abstention never uses the CE (§12.4).
- **What was promoted above gold:**
  - **Bon-Ton.** Eight bankruptcy lease-designation passages ("assignees of the Leases",
    "assumption and assignment of a Lease"): the same topic (assignment), a different legal
    meaning (court-approved assignment of leases, not a restriction on assigning the agreement).
  - **Sucampo.** Lien and covenant boilerplate, a securities-report reference and a publicity
    clause, none about audit or records access.
  - **Theravance.** "No variation or agreed termination", the definitions/interpretation clause,
    and an immediate-termination-for-cause clause. These share "terminate" without answering
    "termination for convenience".
  - **Tate & Lyle.** Termination conditions and a "nothing … shall require" clause; the general
    restriction and its exception are not distinguished.
  - **Depomed.** "'or' is disjunctive but not necessarily exclusive" and other interpretation
    boilerplate. The literal word "exclusive" dominates.
  - **Passport question (`unans-025`).** The CE's top passage is the cover page naming Nigel
    Crockett: an entity match, not evidence.
- **Reading.** The model scores topical and lexical-entity similarity, not whether a passage
  answers the question. Gold texts get strongly negative logits in most cases.

### 13.2 Implementation audit [measured]

| Check | Finding |
|---|---|
| Query given to the CE | the question without the contract preamble; **no** expansion terms (expansion is for BM25 only) |
| Passage text | the whole chunk (≤ 1,000 characters, exact source text); no title or metadata. Routing has already fixed the contract |
| Truncation | 7 of 2,027 chunks exceed 500 tokens (max 805, median 183, p99 373), so truncation at 512 is negligible |
| Gold dilution | gold covers on median **31%** of a gold-overlapping chunk, so the CE scores mostly non-gold text. This is inherent to 1,000-character chunks, not a bug |
| Scores | raw logits, sorted descending, ties broken by BM25 rank; no normalisation needed for ordering |
| Ordering / selection | verified by tests: reranking reorders the top `candidate_k` only; tail order, ids, offsets, text and BM25 scores are preserved; recall@64 is unchanged |
| Discarded passages | none: the candidate set is identical (R@64 0.9517 in B, C, 6b, D) |

**No implementation bug was found.**

### 13.3 Candidate pool [measured]

The rank of the first gold-overlapping chunk in the BM25 order (`candidate_v4`), over 140 train
queries:

| Gold chunk within BM25 top | 1 | 5 | 10 | 20 | 50 | 100 |
|---|---:|---:|---:|---:|---:|---:|
| queries | 93 | 124 | 129 | 133 | 135 | 136 |

Pool sizes vary: the median query has only 27.5 candidates with BM25 > 0, and the maximum is 277.
The first stage is not the bottleneck. BM25 already puts gold at rank 1 for two thirds of the
queries, and enlarging the pool beyond 20 adds only 3 queries. The CE scores of the top 100 for
every train query were cached and replayed exactly through the evaluation code (the replay
reproduces the real exp 6 and 6b runs to four decimals):

| `candidate_k` | P@1 | R@1 | F1@5 | R@5 | R@16 |
|---|---:|---:|---:|---:|---:|
| B (no rerank) | **0.2464** | **0.5508** | **0.1743** | **0.8095** | **0.9186** |
| 10 | 0.1991 | 0.4430 | 0.1553 | 0.7514 | 0.9186 |
| 20 | 0.1874 | 0.4259 | 0.1442 | 0.7102 | 0.9117 |
| 50 | 0.1874 | 0.4259 | 0.1419 | 0.7050 | 0.9001 |
| 100 | 0.1874 | 0.4259 | 0.1412 | 0.7036 | 0.8960 |

Smaller pools hurt less only because the CE can move fewer chunks. No pool size helps, so the
pool size was not changed.

### 13.4 Alternative rerankers

| Model | Domain / training | Size | Licence | Usable here? |
|---|---|---|---|---|
| `cross-encoder/ms-marco-MiniLM-L-6-v2` (C) | MS MARCO web search | 22.7M params, 87 MB | Apache-2.0 (MS MARCO data: non-commercial terms) | evaluated, rejected |
| `Alibaba-NLP/gte-reranker-modernbert-base` (D) | general text reranking (GTE recipe, ModernBERT); strong small-model BEIR/LoCo scores per its card | 149.6M params, 571 MB | Apache-2.0 | **evaluated**: strongest compact permissive general reranker found |
| `lxyuan/LegalBenchRAG-Ettin-150M-Reranker` | fine-tuned on the **full LegalBench-RAG** (incl. 4,042 CUAD questions), split by document | ~150M | Apache-2.0 | **excluded**: its training split is not published, so our 29 contracts and their queries (train *and* test) were very likely in its training data; any score here would be contaminated |
| `BAAI/bge-reranker-v2-m3`, `Qwen3-Reranker-0.6B`, `mxbai-rerank` v2 | general multilingual / LLM-based | 0.5–0.6B+ | Apache-2.0 or MIT (per secondary sources) | not run: 4× the size of D, and D already regressed |
| Jina reranker v2/v3, zerank-2 | general | — | CC-BY-NC-4.0 | excluded (non-commercial) |
| Cohere / Voyage rerank | general (API) | — | paid API | not run; the LegalBench-RAG paper reports Cohere rerank **below** no reranking |

No usable legal-domain cross-encoder was found. The one legal model is contaminated for this
benchmark, and ContractNLI fine-tunes cover only NDA hypotheses.

**D results [measured]** (`artifacts/eval/exp7_D_gte_reranker_train/`, top 50, same settings as C):

| Metric | B | C (MiniLM) | D (gte) |
|---|---:|---:|---:|
| P@1 / R@1 / F1@1 | **0.2464 / 0.5508 / 0.3108** | 0.1874 / 0.4259 / 0.2371 | 0.2196 / 0.4534 / 0.2649 |
| P@2 / R@2 / F1@2 | **0.1827 / 0.6524 / 0.2636** | 0.1370 / 0.5463 / 0.2016 | 0.1540 / 0.5677 / 0.2220 |
| P@5 / R@5 / F1@5 | **0.1049 / 0.8095 / 0.1743** | 0.0841 / 0.7050 / 0.1419 | 0.0971 / 0.7389 / 0.1619 |
| R@10 (top-10 recompute) | **0.8805** | 0.8248 | 0.8371 |
| abstention (FA / CA / BA) | 3/140 · 28/28 · 0.989 | same | same |
| mean query latency | 0.0008 s | 1.02 s | **7.20 s** |
| peak memory | 55 MiB | 945 MiB | 1,440 MiB |

D is better than C but still below BM25 on every metric. On the six audited cases it keeps
Bon-Ton, Sucampo and Tate & Lyle at rank 1, drops Depomed to 8 and Theravance out of the top 10.
**Rejected.** A legal-domain reranker might do better [hypothesis]; none is available
uncontaminated.

### 13.5 Evidence-support verification: approaches compared

| | A. NLI (e.g. DeBERTa-v3 MNLI, 70–440M) | B. Local instruct LLM (Qwen3-1.7B Q8 GGUF) | C. External LLM API |
|---|---|---|---|
| Semantic understanding | sentence-pair entailment; contract passages and question-shaped hypotheses are out of distribution | reads question and passages jointly; can follow "quote the evidence" | strongest [hypothesis] |
| Evidence grounding | none built in (label only) | verbatim quotes, mechanically checked against the source | same quote check applies |
| Question → hypothesis | **required**: either per-question-type templates (hand-written, tunable on train) or a generator | not needed | not needed |
| CPU / RAM | low (0.3–1.7 GB) | 1.83 GB model, 2.5 GB peak RSS | none locally |
| Latency (this CPU) | ~0.1–1 s [hypothesis] | **26.5 s / query** (5 passages, ~1,240 prompt tokens) [measured] | network-bound, ~1–5 s [hypothesis] |
| Cost | free | free | per-token fees |
| Privacy | local | local | contract text leaves the machine |
| Reproducibility | deterministic | greedy decoding + seed + response cache; reproducible on this build | provider models change without notice |
| Deployment | easy | heavy for free CPU hosting | needs API key handling; optional at most |

**Chosen for implementation: B (local LLM).** It is the only option that is free, private and
grounded without hand-written hypothesis templates. NLI was not implemented, because converting
CUAD questions into hypotheses would mean new hand-written, train-tuned rules. The API option was
not implemented: it is costly, sends contract text off the machine, and is not reproducible.

### 13.6 Verifier implementation (`src/verify.py`, optional extra `verify`)

- **Input.** The model sees the full query and the top 5 retrieved passages, verbatim, as
  `<excerpt id="P1..P5">`. It must return JSON with
  `decision ∈ {supported, ambiguous, insufficient}` and verbatim quotes.
- **Output is never trusted as-is.** Malformed JSON, an unknown decision, a fabricated passage id,
  a quote that is not a verbatim (whitespace-insensitive) substring of the cited passage, or
  "supported" without a quote all become `invalid`.
- **Fail-closed.** Failures and timeouts become `error`. Only `supported` can lead to an answer;
  `ambiguous` abstains by default.
- **Traceable evidence.** Valid quotes are mapped to exact source offsets.
- **Prompt injection.** Passages are treated as untrusted. Tag text inside passages is
  neutralised in the prompt, and the quote check prevents injected text from creating support.
- **Not a probability.** No confidence is requested or used.
- **Reproducibility.** Greedy decoding, seed 0, and raw outputs cached by a hash of
  (prompt version, model, settings, prompt). The prompt (`PROMPT_VERSION = "v1"`) was written once
  before the run and not revised after seeing outputs.
- **Modes**, combined with the unchanged BM25 decision:

  | Mode | Answer iff |
  |---|---|
  | `gate` | BM25 answers **and** the verifier supports |
  | `replace` | the query has candidates **and** the verifier supports |
  | `rescue` [post-hoc] | BM25 answers **or** the verifier supports |

  Ranking and retrieval metrics are never changed by the verifier.

### 13.7 Verifier results [measured]

`artifacts/eval/exp8_E_verifier_gate_train/`, `exp8b_E_verifier_replace_train/` and
`exp8c_E_verifier_rescue_posthoc_train/`. One generation pass covered 153 queries (those with
candidates); 8b and 8c replay the same cached outputs. Retrieval metrics are identical to B by
construction.

| Abstention (train) | B | E gate | E replace | E rescue [post-hoc] |
|---|---:|---:|---:|---:|
| false abstentions | 3/140 | 88/140 | 87/140 | **2/140** |
| correct abstentions | 28/28 | 28/28 | 28/28 | 28/28 |
| failures to abstain | 0/28 | 0/28 | 0/28 | 0/28 |
| balanced accuracy | 0.989 | 0.686 | 0.689 | **0.993** |
| answer precision | 1.000 | 1.000 | 1.000 | 1.000 |
| answer recall | 0.979 | 0.371 | 0.379 | 0.986 |
| confusion (ans-answered / ans-abst / unans-answered / unans-abst) | 137/3/0/28 | 52/88/0/28 | 53/87/0/28 | 138/2/0/28 |
| demo A / B / C | 8/10 · 4/4 · 14/14 | not run | not run | 9/10 · 4/4 · 14/14 |

**Verifier decisions.** Over the 153 queries: 53 supported, 89 insufficient, 11 invalid,
0 ambiguous, 0 errors.
- **Too strict.** Of the 124 answerable queries whose gold was in the top 5, the verifier said
  "insufficient" for 63.
- **Invalid outputs.** 11 were invalid because the quote was paraphrased rather than copied
  verbatim. The check worked as designed and failed closed.
- **Quote quality.** Of the 53 supported answerable queries, 37 quotes overlap gold.
- **Negatives.** All 13 negatives with candidates were judged "insufficient".
- **Literal reading.** It is too literal in the same way as BM25. For Theravance it answered
  "none of the excerpts explicitly mention termination for convenience".

**BicycleTX (E1) vs `unans-025` [measured].** The verifier separates the pair, which no lexical or
CE signal did:
- E1 is "supported", quoting "All IPRs subsisting in any Works shall be the exclusive property of
  the Company."
- The passport query is "insufficient", because no excerpt contains the details.

So E1 is an **abstention** problem, not a ranking problem: gold is at rank 1. Rescue mode answers
E1 and nothing else changes.

**Operational [measured].**

| Item | Value |
|---|---|
| model file | 1,834,426,016 bytes |
| first load incl. download | 928 s (about 2 MB/s); cached load 0.6 s |
| mean generation | 26.5 s per verified query |
| peak RSS | 2.5 GiB |
| full train pass | about 68 min on the i5-10400 (6 cores, AVX2, no BF16) |
| API cost | 0 |

### 13.8 Decision and recommendations

- **Rerankers C (MiniLM) and D (gte): rejected [measured].** Both are worse than BM25 at every
  k ≤ 10, and no pool size helps. The reranker code stays, off by default.
- **F (reranker + verifier): not run.** Its prerequisite, a reranker that helps on its own, was
  not met.
- **Verifier gate/replace: rejected [measured].** Precision is perfect but recall is too low
  (0.37–0.38).
- **Verifier rescue: promising but NOT promoted [post-hoc].**
  - Fixes the one known false abstention (BicycleTX) with no new failure to abstain.
  - The evidence is thin: the mode was chosen after seeing train results, and only 3 BM25 false
    abstentions and 13 negatives with candidates exercise it.
  - In interactive search it runs only when BM25 abstains with candidates (16/168 train
    queries), so the extra latency (about 26 s on this CPU) affects only those queries.
  - Before any promotion it needs a pre-registered evaluation on new data: a fresh, frozen set of
    unanswerable queries written before running it, especially near-miss negatives about real
    contracts like `unans-025`.
- **`configs/candidate_v4.yaml` remains the best measured train configuration;
  `configs/final.yaml` remains the tested one.** Neither was changed. *(Superseded on
  2026-11-06: `candidate_v4` was test-evaluated and promoted to `configs/final.yaml`, §14.)*
- **Future [hypothesis].**
  - A larger local model (4–8B) or an API backend may reduce the verifier's strictness.
  - Sentence-window scoring (instead of 1,000-character chunks) may help any reranker, given the
    31% gold dilution.
  - An uncontaminated legal-domain reranker is the only reranking direction still worth testing.

**Reproduce:**
```bash
uv sync --extra dense --extra verify
python -m pytest -q                                   # 166 passed, 1 xfailed
python -m src.cli validate-data
python -m src.cli evaluate --config configs/experiments/exp7_gte_reranker.yaml --out artifacts/eval/<new>_D
python -m src.cli evaluate --config configs/experiments/exp8_verifier_gate.yaml --out artifacts/eval/<new>_E_gate
python -m src.cli evaluate --config configs/experiments/exp8b_verifier_replace.yaml --out artifacts/eval/<new>_E_replace
python -m src.cli evaluate --config configs/experiments/exp8c_verifier_rescue.yaml --out artifacts/eval/<new>_E_rescue
python -m src.cli compare artifacts/eval/exp6_A_final_train artifacts/eval/exp6_B_candidate_v4_train \
  artifacts/eval/exp6_C_cross_encoder_train artifacts/eval/exp7_D_gte_reranker_train \
  artifacts/eval/exp8_E_verifier_gate_train artifacts/eval/exp8b_E_verifier_replace_train \
  artifacts/eval/exp8c_E_verifier_rescue_posthoc_train \
  --qids cuad-51b4e44436 cuad-0f789ebcf3 cuad-05251665f3 cuad-3fdb534e55 cuad-5fce387d80 cuad-7646cba011 unans-025
python -m src.cli demo-check --config configs/experiments/exp8c_verifier_rescue.yaml
```
The verifier cache lives under `artifacts/cache/verifier/` (gitignored). Without it, the E runs
regenerate, taking about 70 minutes on this CPU.

## 14. Test-split comparison and promotion of `candidate_v4` to final (2026-11-06)

`configs/candidate_v4.yaml` was evaluated on the held-out test split together with the previous
final configuration and the three experimental second stages, and was then promoted to
`configs/final.yaml`. No code, threshold or setting was changed in response to any test result:
the promoted file has exactly the settings that were tested (§14.5).

### 14.1 Test runs #4–#9

`artifacts/test_runs.jsonl`; all on the same 54 answerable / 7 unanswerable test queries, with the
train-calibrated threshold 0.2739 taken from the config (never re-calibrated on test):

| # | Time (IST, 2026-11-06) | Config | Fingerprint | Output (`artifacts/eval/`) | Purpose |
|---|---|---|---|---|---|
| 4 | 10:54:52 | `overlap_up` (previous final) | `e1c913da…` | `overlap_up_test_20261106-105452` | reproduction check of run #2 |
| 5 | 11:14:53 | `candidate_v4` | `8f6d2afd…` | `cmp_test_B_candidate_v4` | test result of the train-selected candidate |
| 6 | 11:48:52 | `exp8c_verifier_rescue` | `322943cf…` | `cmp_test_C_verifier_rescue` | reporting run, experiment not promoted on train |
| 7 | 12:20:22 | `exp6_cross_encoder` (MiniLM) | `1b09d5dc…` | `cmp_test_C_cross_encoder` | reporting run, rejected on train (§12) |
| 8 | 12:29:23 | `exp7_gte_reranker` | `0db19cf6…` | `cmp_test_D_gte_reranker` | reporting run, rejected on train (§13) |
| 9 | 12:45:31 | `final_v4` (promoted `configs/final.yaml`) | `8f6d2afd…` | `final_v4_test` | confirmation of the promoted file: top-1 changed on 0/61 queries, all metrics identical to #5 |

**Run #4 reproduces run #2 exactly:** top-1 passage changed on 0/61 queries and every metric is
identical. Its fingerprint differs from run #2's (`3254f317…`) only because the config loader
now fills in defaults for keys added later (`require_contract`, `refine`, …) that do not change
results for these queries (§10.5).

### 14.2 Results (test)

Sources: `metrics.json` in each output directory; side-by-side tables in
`artifacts/eval/cmp_test_comparison.json` and `artifacts/eval/cmp3_test.json`.

| Test metric | Previous final | **`candidate_v4`** | + MiniLM reranker | + gte reranker | + verifier rescue |
|---|---:|---:|---:|---:|---:|
| precision@1 | 0.1788 | **0.2638** | 0.1798 | 0.1869 | 0.2638 |
| recall@1 | 0.4328 | **0.5880** | 0.4373 | 0.4270 | 0.5880 |
| precision@5 | 0.0947 | **0.1011** | 0.0975 | 0.0910 | 0.1011 |
| recall@5 | 0.7144 | **0.7821** | 0.7207 | 0.6855 | 0.7821 |
| F1@5 | 0.1514 | **0.1607** | 0.1535 | 0.1431 | 0.1607 |
| recall@10 (recomputed) | 0.7580 | 0.8170 | 0.8199 | **0.8291** | 0.8170 |
| false / correct abstentions | 1/54 · 7/7 | 1/54 · 7/7 | 1/54 · 7/7 | 1/54 · 7/7 | 1/54 · 7/7 |
| mean time per query | 0.0006 s | 0.0007 s | 0.67 s | 8.86 s | 31.6 s per verified query |
| peak memory | 55 MB | 55 MB | 871 MB | 1.4 GB | 2.5 GB |


The train-split comparison of the same configs (`artifacts/eval/cmp3_train.json`, §12–§13) points
the same way: `candidate_v4` F1@5 0.1743 vs 0.1419 (MiniLM) and 0.1619 (gte).

### 14.3 Per-query reading (test)

- **`candidate_v4` vs previous final (recall@5):** 7 better, 3 worse, 44 unchanged. The three
  regressions are `cuad-278b8ff2d7` (minimum commitment, 0.64 → 0.40), `cuad-acff5fc189`
  (licenses granted, 0.78 → 0.70) and `cuad-bfb849cbfd` (post-termination services, 1.00 → 0.76).
- **Remaining misses:** 9/54 answerable test queries have recall@5 = 0 under `candidate_v4`:
  post-termination services (×2), exclusivity, non-compete, covenant not to sue, expiration
  date, volume restrictions, anti-assignment and right of first refusal. Almost all are
  clause-presence questions whose clause text does not share the question's vocabulary.
- **Rerankers vs `candidate_v4`:** MiniLM recall@1 better on 4 / worse on 16, recall@5 better on
  3 / worse on 9, and it fixes 0 of the 9 misses; gte recall@1 better on 8 / worse on 20,
  recall@5 better on 6 / worse on 12, fixes 2 of the 9. The small recall@10 gain comes from
  pulling passages from deep in the top-50 pool into ranks 6–10, below what the user sees.
- **Verifier rescue:** identical to `candidate_v4` on every metric. The only false abstention
  (`cuad-be34fdefc9`, Depomed right of first refusal, signal 0.256) was judged "insufficient", so
  nothing was rescued. Over the 57 verified queries it said "supported" on 27 answerable,
  "insufficient" on 25 answerable (24 of which BM25 answered correctly), "invalid" on 2, and
  "insufficient" on all 3 negatives it saw. The other 4 negatives abstain earlier with
  `contract_not_identified`. The 9/10 demo result (§13.7) did not carry over to test.

### 14.4 Protocol caveats

- **Test reuse.** The test split has been evaluated nine times. The promotion decision was made
  after seeing run #5, so the final configuration's test numbers are **not a fully blind
  estimate**. Mitigations: `candidate_v4` was selected on train before run #5 (§11); its test
  gain matches the train gain in direction; nothing was tuned after any test run; runs #6–#8
  concern experiments already rejected or not promoted on train and drove no decision; run #9
  only re-ran the promoted file and reproduced #5.
- **Few negatives.** Only 7 unanswerable test queries; 4 of them abstain through contract
  identification, so only 3 exercise the score threshold. 7/7 is weak evidence.
- **Small differences.** With 54 answerable queries, changes of one or two queries are within
  noise; the recall@1 gain (+0.155) is the robust part of the result.
- **Any future change** should be developed on train and evaluated on new data, since this test
  split is no longer clean.

### 14.5 Promotion

- `configs/final.yaml` now holds the `candidate_v4` settings with `name: final_v4`,
  `status: final`. `name` and `status` are excluded from the fingerprint, so its fingerprint is
  `8f6d2afd50a4819e`, identical to run #5. This is enforced by
  `tests/test_end_to_end.py::test_promoted_final_config_matches_tested_candidate_v4`.
- The previous final is archived unchanged (except `status: archived` and a header comment) at
  `configs/archive/final_overlap_up.yaml`; its fingerprint is still `e1c913daee266b6c` (run #4).
- `configs/candidate_v4.yaml` is kept, with identical settings, because the experiment configs
  and earlier commands reference it.
- The CLI default (`src/cli.py`) and the app default (`app.py`, `CIA_CONFIG`) are
  `configs/final.yaml`, so both now use the promoted configuration. Demo check with the new
  final: A 8/10, B 4/4, C 14/14. Tests: 167 passed, 1 xfailed (BicycleTX, a train query, §11.8).
- The reranker and the verifier stay off in every non-experiment config.

**Reproduce (no new test run needed):**
```bash
python -m pytest -q                                   # 167 passed, 1 xfailed
python -m src.cli demo-check                          # final: A 8/10, B 4/4, C 14/14
python -m src.cli compare artifacts/eval/overlap_up_test_20261102-153405 \
  artifacts/eval/overlap_up_test_20261106-105452 artifacts/eval/cmp_test_B_candidate_v4 \
  artifacts/eval/cmp_test_C_cross_encoder artifacts/eval/cmp_test_D_gte_reranker \
  artifacts/eval/cmp_test_C_verifier_rescue
```
