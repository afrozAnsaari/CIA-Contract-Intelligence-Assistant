# Contract Intelligence Assistant (CIA)

Searches commercial contracts for passages that answer a natural-language question. It returns
verbatim passages with the source document ID and exact character offsets, or explicitly
**abstains** when the indexed contracts don't contain enough relevant evidence. Evaluated on
LegalBench-RAG-mini (CUAD subset: 194 queries, 29 contracts) with the benchmark's character-level
precision and recall. Results and analysis are in **[REPORT.md](REPORT.md)**.

> Retrieval aid only, not legal advice.

- Lexical BM25 retrieval (no GPU, no API keys, no LLM), routed to the contract named in the query.
- Offset-preserving chunking: `source[start:end] == passage` is enforced for every result.
- Abstention with a train-calibrated threshold, evaluated on a 35-query unanswerable set.
- A deterministic, train-only improvement loop that logs every accepted and rejected candidate.
- CLI and Streamlit app that share one pipeline.

## Setup

Requirements: Linux/macOS, Python ≥ 3.13, [uv](https://docs.astral.sh/uv/). No environment
variables or secrets are needed (the optional `CIA_CONFIG` selects the app's config).

```bash
git clone <repo-url> CIA && cd CIA
uv sync                      # core + dev deps from uv.lock  (pip alternative: pip install -r requirements.txt)
source .venv/bin/activate    # or prefix commands with `uv run`
# optional, only for dense/hybrid experiments (CPU torch, ~1-3 GB download):
uv sync --extra dense
```

`pyproject.toml` + `uv.lock` are the source of truth. `requirements.txt` is exported from them:
`uv export --no-hashes --all-extras --all-groups -o requirements.txt && sed -i '1i --extra-index-url https://download.pytorch.org/whl/cpu' requirements.txt`.

### Data

Download the public LegalBench-RAG dataset (any location). Only `benchmarks/cuad.json` and
`corpus/cuad/` are used. Then copy the needed files into the repo (byte-identical, checksum
verified, idempotent; `data/raw/` is gitignored):

```bash
python -m src.cli prepare-data --source /path/to/legalbench-rag
python -m src.cli validate-data
```

## Usage

All commands run from the repository root.

```bash
# CLI search
python -m src.cli search \
  --query "Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; What is the governing law for this contract?" \
  --top-k 5
python -m src.cli search \
  --query "Who won the FIFA World Cup in 2018?" \
  --top-k 5                       # -> ABSTAINED
python -m src.cli search --query "..." --top-k 3 --json        # machine-readable
python -m src.cli search --query "What is the governing law for this contract?" --document PapaJohns
                                  # --document restricts to one contract (id or unique substring)
python -m src.cli search --query "..." --config configs/baseline.yaml
python -m src.cli show-span --document PapaJohns --start 63649 --end 63806   # print a source slice

# Web app (http://localhost:8501)
streamlit run app.py
CIA_CONFIG=configs/baseline.yaml streamlit run app.py

python -m src.cli --help          # all subcommands
```

| Subcommand | Purpose |
|---|---|
| `prepare-data --source DIR` | copy `cuad.json` + the 29 referenced contracts into `data/raw/`, write `data/processed/manifest.json` |
| `validate-data` | mini selection, split, gold offsets, negative set, chunk offsets |
| `build-index` | chunk + index, write `artifacts/index/<fingerprint>/{chunks.jsonl,stats.json}` |
| `search` | query the pipeline (same code path as the web app) |
| `evaluate [--split test --final-test]` | per-query + aggregate metrics; train calibrates the threshold, test never does |
| `improve` | the one-command train-only improvement loop |
| `error-analysis` | categorised train failures (`error_analysis.md`, `failures.jsonl`) |
| `demo-check` | PASS/FAIL battery: train queries, train negatives, invalid inputs |
| `show-span --document D --start S --end E` | print `document[S:E]` from the original source text (offset checks) |

The CUAD-style query format "Consider the <contract>; <question>" works best: the preamble picks
the contract and the question ranks its passages. With the final config, a question that names no
contract **abstains** with reason `contract_not_identified` and suggests the closest contracts.
You can name the contract in the question, pass `--document`, or pick it in the app sidebar.

## Architecture

```
src/
  config.py           defaults + YAML + dotted overrides; config/index fingerprints
  data.py             mini(), assign_split() (verbatim protocol), prepare/load/validate
  text.py             search-only tokenisation (lowercase/stopwords/Snowball), query split
  chunking.py         boundary-aware, offset-preserving chunker
  retrieval.py        in-house BM25, document routing, optional dense + hybrid RRF, overlap policy
  abstention.py       decision rule + train calibration (single and two-threshold)
  pipeline.py         the single query pipeline (CLI, app and evaluation all call it)
  metrics.py          character-level P/R/F1@k (set-based) + reference pairwise variant
  evaluation.py       per-query/aggregate results, artifacts, test-run counter
  diagnostics.py      failure categories and error-analysis artifacts
  improvement_loop.py deterministic train-only loop with an acceptance rule
  demo_check.py       manual acceptance battery
  cli.py              argparse CLI (`python -m src.cli ...`)
app.py                Streamlit UI
configs/              baseline.yaml, final.yaml, loop.yaml (protocol + candidates)
data/unanswerable_queries.json   frozen negative set (v1.0, 35 queries)
tests/                pytest suite (synthetic fixtures + `real_data` tests)
artifacts/            eval/, loop/, error_analysis/, test_runs.jsonl (indexes are gitignored)
```

Data flow: query → split preamble/question → document BM25 on the preamble picks one contract →
chunk BM25 on the question ranks that contract's chunks → overlap trimming → top-k passages
(exact offsets) → abstention check on the full query's normalised BM25 score.

### Configuration

| File | Meaning |
|---|---|
| `configs/baseline.yaml` | initial BM25 config (1,000/150 chunks, full query); threshold written by `evaluate --write-threshold` |
| `configs/final.yaml` | selected by loop run 3 (`overlap_up`): question-only ranking, routing, stemming + stopwords, 1,000/300 chunks, trim, `chunk_full_bm25_norm` ≥ 0.2739; plus `require_contract: true` added after the test runs (no effect on benchmark queries, REPORT.md §10) |
| `configs/loop.yaml` | primary metric, guardrails, tolerances, candidate list (spec v3, with change log) |

Every key and its default is listed in `src/config.py` (`DEFAULTS`). Any key can be changed in
YAML without editing code.

## Manual runbook (commands to execute locally)

From the repo root with the venv active. Runtimes were measured on a 12-core CPU laptop.

| # | Step | Command | Expected output / artifacts | Success check | Cost |
|---|---|---|---|---|---|
| 1 | Install | `uv sync` (optional `uv sync --extra dense`) | `.venv/` | `python -c "import streamlit, numpy, yaml, snowballstemmer"` | ~1 min; dense extra 1-3 GB |
| 2 | Data | `python -m src.cli prepare-data --source /path/to/legalbench-rag` | `data/raw/legalbench-rag/...`, `data/processed/manifest.json`, `cuad_mini_queries.jsonl` | `mini_n: 194`, `n_documents: 29`, `train: 140`, `test: 54`, `checksums_verified: 30` | seconds |
| 3 | Validate | `python -m src.cli validate-data` | JSON report | `gold_spans_mismatched: 0`, `indexed_equals_referenced: true`, `n_unanswerable: 35` (28/7), `unanswerable_absence_term_hits: {}`, `chunk_offset_violations: 0`, `VALIDATION OK` | < 1 s |
| 4 | Freeze negatives | `git add data/unanswerable_queries.json && git commit -m "Freeze unanswerable set"` | commit | never edited afterwards (each loop run records its SHA-256) | - |
| 5 | Tests | `python -m pytest -q` | - | `83 passed` | ~2 s |
| 6 | Index | `python -m src.cli build-index --config configs/final.yaml` | `artifacts/index/<fp>/stats.json` | `n_documents: 29`, `n_chunks: 2027` (baseline: 1617) | seconds |
| 7 | Baseline train eval | `python -m src.cli evaluate --config configs/baseline.yaml` | `artifacts/eval/baseline_train_<ts>/{metrics.json,metrics_by_k.csv,per_query.jsonl,config_used.yaml}` | `answerable n=140 unanswerable n=28 offset_errors=0`, F1@5 0.0328 | seconds |
| 8 | Improvement loop | `python -m src.cli improve --config configs/baseline.yaml --spec configs/loop.yaml --run-name run3` | `artifacts/loop/run3/{loop.log,iterations.jsonl,accepted_config.yaml,summary.json,iterNN_*/}` | ends with `[loop] done. evaluated=12 accepted=overlap_up`, exit 0 | ~4 s (dense candidates skipped unless the extra is installed) |
| 9 | Inspect | `python -c "import json;[print(r.get('iteration'),r['candidate_id'],r['decision'],r['reason']) for r in map(json.loads,open('artifacts/loop/run3/iterations.jsonl'))]"` | - | every candidate has a decision + reason | - |
| 10a | Promote | `cp artifacts/loop/run3/accepted_config.yaml configs/final.yaml`, then set `status: final` and add `require_contract: true` under `query:`; commit | - | `demo-check` C = 13/13 | - |
| 10b | Final test (once) | `python -m src.cli evaluate --config configs/final.yaml --split test --final-test` | `artifacts/eval/<name>_test_<ts>/`, appends to `artifacts/test_runs.jsonl` | `answerable n=54 unanswerable n=7`, threshold "(from config)" | seconds |
| 10c | Baseline test | `python -m src.cli evaluate --config configs/baseline.yaml --write-threshold` then `... --config configs/baseline.yaml --split test --final-test` | as above | test run recorded | seconds |
| 11 | Error analysis | `python -m src.cli error-analysis --config configs/final.yaml` (and `baseline.yaml`) | `artifacts/error_analysis/<name>/{error_analysis.md,failures.jsonl,summary.json}` | ≥ 10 failures, grouped | seconds |
| 12 | Demo | `python -m src.cli demo-check --config configs/final.yaml`; `streamlit run app.py`; CLI examples above | console / browser | demo-check: A 4/10, B 4/4, C 13/13; GUI: green passages for `[PASS] A` queries, "Abstained" for B queries, "Abstained - which contract?" with suggestions for a question naming no contract, warning on empty input | seconds |
| 13 | Final checks | `python -m pytest -q`; `git status`; `git ls-files \| grep -Ei "data/raw\|artifacts/index\|\.env\|\.pdf\|prompt.md"` | - | tests pass; the grep prints nothing | - |

Safety rails: the test split can't be evaluated without `--final-test`, and each test run is
counted in `artifacts/test_runs.jsonl`. The loop removes test queries before it starts.

### Reproducing the reported numbers

Steps 2 → 3 → 7 → 8 → 10a → 10b → 10c → 11. All components are deterministic (fixed tie-breaking,
no sampling), so re-running reproduces the logged metrics exactly. Loop runs `run2` (re-run with
spec v3) and `run3` produced identical decisions.

## Testing

`python -m pytest -q` runs 83 tests in about 2 seconds:
- **Synthetic fixtures:** unit tests for metrics (exact, partial, extra text, wrong document,
  multiple spans, overlap, empty, k cutoffs), chunk offsets, BM25 (against a hand-computed
  score), tie handling, abstention (equality, no candidates, two-threshold rule, calibration),
  the loop (train-only, logging, never overwrites the accepted config, frozen set, reproducible),
  and end to end (CLI, headless Streamlit `AppTest`, evaluation files, test-split refusal).
- **`real_data` tests:** checks against the real data that skip if `data/raw` is missing.
- **Dense/hybrid:** tested with a stub encoder, so no model download is needed.

## Assumptions and limitations

- Character offsets follow Python default text-mode UTF-8 reading (universal newlines), as the
  benchmark specifies. Gold spans were validated 272/272.
- Metrics use the union of character intervals (no double counting). The authors' pairwise
  variant is reported alongside and is identical here, because returned passages never overlap.
- F1@5 (per-query harmonic mean, averaged) is the selection objective. It is not a benchmark metric.
- Contract identity comes from the query's "Consider …;" preamble or an explicit `--document`
  or sidebar choice. Unnamed contracts abstain (`contract_not_identified`); free-form references
  are not resolved.
- Dense and hybrid retrieval are implemented but were not evaluated. No LLM is used.
- The unanswerable set (35 queries, 7 in test) was hand-authored and checked lexically against
  the indexed corpus only. That check is not a legal determination.

More detail is in REPORT.md §9.

## AI-tool usage

This project was built with **Claude Code (Anthropic, Claude Opus 5.5)** as a pair-programmer:
- **AI-drafted:** module code, tests, configs, the unanswerable query set (with lexical absence
  checks against the corpus), and drafts of this README and REPORT.md.
- **Done by the author:** all dependency installs, data preparation, test runs, evaluations,
  improvement-loop runs and the final test evaluation were run locally by the author, and the
  results were pasted back for analysis.
- **Fixed after inspection:** design changes after loop run 1 (question-only ranking with
  full-query abstention) came from inspecting train diagnostics together. AI-suggested example
  queries that turned out not to work were caught by the author and fixed. This is why the
  `demo-check` battery exists.
- **Responsibility:** the author reviewed the implementation and is responsible for it. No
  contracts or data were sent to any service other than the coding assistant session.
