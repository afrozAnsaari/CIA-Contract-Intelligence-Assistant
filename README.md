# Contract Intelligence Assistant

A retrieval assistant for commercial contracts, built for the LegalBench-RAG-mini **CUAD** subset
(194 queries over the 29 contracts they reference). For a natural-language question it returns
ranked **verbatim evidence passages**: document ID, exact character offsets into the original
contract text, passage text, score and rank. When the indexed contracts don't contain enough
supporting evidence, it **abstains** and returns no passages.

It is a lexical retrieval system (BM25). It doesn't use an LLM, doesn't generate answers and
doesn't interpret contracts. It is a retrieval aid, not legal advice.

Evaluation methodology, measured results, experiment history and failure analysis are in
[REPORT.md](REPORT.md).

## Features

- **Prescribed data selection.** Queries come from `benchmarks/cuad.json` via the prescribed
  `mini()` function. Only the contracts those queries reference are indexed. Train and test are
  assigned by the prescribed SHA-256 rule ([`src/data.py`](src/data.py)).
- **Offset-preserving passages.** Contracts are split into boundary-aware chunks whose offsets
  index the unmodified source text. Every returned passage is checked to satisfy
  `source_text[start_offset:end_offset] == text` ([`src/chunking.py`](src/chunking.py),
  [`src/pipeline.py`](src/pipeline.py)).
- **Ranked results.** Each passage has `rank`, `document_id`, `start_offset`, `end_offset`,
  `text`, `score` and `chunk_id`. Ties are broken deterministically.
- **Contract routing.** For queries of the form `Consider the <contract>; <question>`, the
  contract description selects one contract, and passages inside it are ranked
  ([`src/retrieval.py`](src/retrieval.py)).
- **Abstention.** A configurable threshold over a normalised BM25 evidence score, calibrated on
  training data only. The configuration can also be set to abstain, with suggestions, when a
  question doesn't name a contract ([`src/abstention.py`](src/abstention.py)).
- **Evaluation.** Character-level precision and recall at k = 1, 2, 4, 5, 8, 16, 32, 64, plus
  abstention metrics on answerable queries and on a separate set of unanswerable queries
  ([`src/metrics.py`](src/metrics.py), [`src/evaluation.py`](src/evaluation.py)).
- **Self-improvement loop.** A deterministic, train-only loop. It evaluates predeclared candidate
  changes against an acceptance rule and logs every hypothesis, change, metric and decision
  ([`src/improvement_loop.py`](src/improvement_loop.py), [`configs/loop.yaml`](configs/loop.yaml)).
- **Interfaces.** A CLI and a Streamlit web app that call the same `Pipeline.search`.
- **Validation and tests.** Data validation, a PASS/FAIL demo battery, and a pytest suite.

Dense (sentence-transformers) and hybrid reciprocal-rank-fusion retrieval are implemented as an
optional extra, but are not part of the evaluated configurations.

## Requirements and setup

- Python **≥ 3.13** (`pyproject.toml`)
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- CPU only; no GPU, API keys or network access are needed at runtime

```bash
git clone <repository-url> CIA && cd CIA
uv sync                         # installs core + dev dependencies from uv.lock
source .venv/bin/activate       # or prefix every command with `uv run`
```

The alternative with pip is `pip install -r requirements.txt`. That file is exported from
`uv.lock` and includes the optional dense extra (CPU PyTorch). With uv, the optional dense/hybrid
dependencies are installed with `uv sync --extra dense`.

**Environment variables:** none are required. `CIA_CONFIG` optionally selects the config used by
the web app (default `configs/final.yaml`).

### Benchmark data

The data isn't included in this repository. Download the public **LegalBench-RAG** dataset
separately. Only `benchmarks/cuad.json` and `corpus/cuad/` are used. CUAD is distributed under
CC BY 4.0 and the LegalBench-RAG queries under MIT, as stated in the dataset's `LICENSE` file.
Follow those terms.

Copy the required files into the repository. The copy is byte-identical, checked against the
dataset's `SHA256SUMS`, and idempotent; `data/raw/` is gitignored.

```bash
python -m src.cli prepare-data --source /path/to/legalbench-rag
```

This writes `data/raw/legalbench-rag/{benchmarks/cuad.json, corpus/cuad/*.txt}` (only the
referenced contracts), `data/processed/manifest.json` and
`data/processed/cuad_mini_queries.jsonl`. The frozen unanswerable-query set is committed at
[`data/unanswerable_queries.json`](data/unanswerable_queries.json).

## Running the assistant

Run all commands from the repository root.

**CLI**

```bash
python -m src.cli search \
  --query "Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; What is the governing law for this contract?" \
  --top-k 5
```

| Option | Meaning |
|---|---|
| `--query/-q` | the question (required) |
| `--top-k/-k` | maximum number of passages (default 5); fewer are returned when fewer passages match |
| `--document/-d` | restrict to one contract (exact `document_id` or unique substring, e.g. `PapaJohns`) |
| `--config` | config file (default `configs/final.yaml`) |
| `--json` | machine-readable output |

The output states whether the system **answered** or **abstained** (with the evidence score and
threshold), followed by the ranked passages and their document IDs and `[start, end)` offsets. If
a question names no contract and the config has `query.require_contract: true`, the system
abstains with reason `contract_not_identified` and lists the closest contracts.

To print an exact span from an original contract (useful for checking offsets):

```bash
python -m src.cli show-span --document PapaJohns --start 63649 --end 63806
```

**Web app**

```bash
streamlit run app.py                                  # http://localhost:8501
CIA_CONFIG=configs/baseline.yaml streamlit run app.py # use another config
```

The sidebar shows the active config, the number of indexed contracts and chunks, a top-k slider,
and an optional contract selector. Restart the app after editing a config, because the pipeline
is cached.

## Running the evaluation

```bash
python -m src.cli evaluate --config configs/baseline.yaml                 # train split (default)
python -m src.cli evaluate --config configs/final.yaml --no-calibrate     # train, use stored threshold
python -m src.cli evaluate --config configs/final.yaml --split test --final-test
```

- On **train**, the abstention threshold is recalibrated unless you pass `--no-calibrate`.
  `--write-threshold` stores the calibrated value back into the config.
- **Test** is never recalibrated. It requires `--final-test`, and each test run is appended to
  `artifacts/test_runs.jsonl`.
- **Output** goes to `artifacts/eval/<config-name>_<split>_<timestamp>/` (or `--out DIR`):
  `metrics.json` (aggregates with query counts), `metrics_by_k.csv`, `per_query.jsonl` and
  `config_used.yaml`.
- **Metrics:**
  - character-level precision@k = retrieved gold characters / retrieved characters
  - recall@k = retrieved gold characters / gold characters, over the top-k passages
  - F1@k, the per-query harmonic mean used as the selection objective
  - abstention metrics: false-abstention rate on answerable queries; correct-abstention and
    failure-to-abstain rates on unanswerable queries; balanced accuracy

  Exact definitions are in [REPORT.md §6](REPORT.md#6-output-format-and-evaluation-definitions).

**Improvement loop** (train only):

```bash
python -m src.cli improve --config configs/baseline.yaml --spec configs/loop.yaml --run-name <name>
```

This writes `artifacts/loop/<name>/` containing `loop.log`, `iterations.jsonl` (one record per
candidate), `accepted_config.yaml`, `summary.json` and one directory per evaluated iteration.
Reusing a `--run-name` overwrites that directory.

**Error analysis** (train only):

```bash
python -m src.cli error-analysis --config configs/final.yaml
```

This writes `artifacts/error_analysis/<config-name>/` containing `error_analysis.md`,
`failures.jsonl` and `summary.json`.

## Running tests and validation

```bash
python -m pytest -q                                        # automated test suite
python -m src.cli validate-data                            # data integrity checks
python -m src.cli demo-check --config configs/final.yaml   # PASS/FAIL battery (train data only)
python -m src.cli build-index --config configs/final.yaml  # chunk statistics -> artifacts/index/
```

- **`pytest`** uses small synthetic fixtures. Tests marked `real_data` run only when `data/raw/`
  has been prepared.
- **`validate-data`** checks the 194-query mini selection, the split, the
  indexed-equals-referenced document set, every gold span against the source text, the
  unanswerable set (count, uniqueness, rationale, absence terms) and the chunk offsets. It ends
  with `VALIDATION OK` or `VALIDATION FAILED`.
- **`demo-check`** runs three groups through `Pipeline.search`: fixed train queries, one train
  negative per category, and invalid or unusual inputs. Group C failures indicate bugs; groups A
  and B measure retrieval and abstention quality.

## Architecture

```
src/data.py          load cuad.json -> mini() -> splits; load referenced contracts (unmodified)
src/chunking.py      boundary-aware chunks with exact [start, end) offsets
src/text.py          search-only tokenisation; "Consider ...;" query parsing
src/retrieval.py     BM25 index; contract routing; ranking; overlap handling; signals
src/abstention.py    threshold decision and train-only calibration
src/pipeline.py      Pipeline.search: the single entry point for the CLI, app and evaluation
src/metrics.py       character-level P/R/F1@k and abstention metrics
src/evaluation.py    per-query + aggregate results, artifacts, test-run log
src/diagnostics.py   failure categories, error-analysis artifacts
src/improvement_loop.py  train-only candidate evaluation and acceptance
src/cli.py, app.py   CLI and Streamlit front ends
```

The flow for each query:
1. Parse the optional contract preamble.
2. Select the contract (or use an explicit `--document`).
3. Rank that contract's chunks with BM25.
4. Remove overlapping same-document passages.
5. Compute the evidence score and decide whether to abstain.
6. Return the passages, or an abstention.

All parameters are in YAML configs ([`configs/`](configs/)); defaults are in
[`src/config.py`](src/config.py).

| Config | Purpose |
|---|---|
| [`configs/baseline.yaml`](configs/baseline.yaml) | initial BM25 configuration |
| [`configs/final.yaml`](configs/final.yaml) | configuration selected by the improvement loop (see REPORT.md) |
| [`configs/loop.yaml`](configs/loop.yaml) | loop protocol (primary metric, guardrails) and candidate list, with change log |

## Assumptions and limitations

- **Scope:** only the 29 CUAD contracts referenced by the 194 mini queries are indexed. Results
  say nothing about other contracts or document types.
- **Offsets:** offsets are Python string indices into the contract as read by
  `open(path, encoding="utf-8").read()` (default text mode, universal newlines). Byte offsets or
  other readers may differ.
- **Contract identity:** this comes only from a `Consider …;` preamble or an explicit contract
  choice. Free-form references to a contract aren't resolved.
- **Lexical retrieval:** passages are found by word overlap. A returned passage isn't necessarily
  legally relevant or complete, and an abstention doesn't prove a clause is absent.
- **Scores:** evidence scores and thresholds are not probabilities.
- **Accuracy:** see [REPORT.md](REPORT.md) for measured accuracy and known failure modes before
  relying on results.

## AI tool usage

This project was developed with **Claude Code** (Anthropic) as an AI coding assistant.
- **Drafted with the assistant:** most of the source code, tests, configurations, the
  unanswerable-query set and the documentation, under the developer's direction and review.
- **Run by the developer locally:** dependency installation, data preparation, evaluations,
  improvement-loop runs and test-set evaluations. The developer shared the outputs back during
  development.
- **Responsibility:** the developer is responsible for understanding, explaining and maintaining
  the implementation.

## Report

For methodology, results, experiment history, evaluation-integrity disclosures, failure analysis
and limitations, see **[REPORT.md](REPORT.md)**.
