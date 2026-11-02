# Contract Intelligence Assistant (CIA)

Finding the clause that answers a question in a long commercial contract is slow and easy to get
wrong. CIA retrieves **exact evidence passages** from commercial contracts for a natural-language
question:
- each passage is returned verbatim, with its document ID and exact source **character offsets**;
- when the indexed contracts don't hold enough evidence, the system **abstains** explicitly
  instead of returning weak passages.

**Dataset:** LegalBench-RAG-mini, CUAD subset (194 queries over the 29 contracts they reference).

**Results and analysis:** measured results, the experiment history, failure analysis and
protocol disclosures are in **[REPORT.md](REPORT.md)**.

CIA is a retrieval aid. It doesn't interpret contracts and doesn't give legal advice.

## Key capabilities

- **BM25 lexical retrieval:** an in-house Okapi BM25 over contract chunks
  ([`src/retrieval.py`](src/retrieval.py)).
- **Contract routing:** a query of the form `Consider the <contract>; <question>` is routed to
  one contract using its preamble, and passages are ranked inside that contract. A contract can
  also be selected explicitly.
- **Offset-preserving chunking:** chunks are exact slices of the unmodified source text, and
  every returned passage is checked against the source ([`src/chunking.py`](src/chunking.py),
  [`src/pipeline.py`](src/pipeline.py)).
- **Train-calibrated abstention:** a threshold over a normalised BM25 evidence score, calibrated
  on training data only. A question that names no contract can be set to abstain with
  suggestions ([`src/abstention.py`](src/abstention.py)).
- **Deterministic, train-only improvement loop:** predeclared candidate changes, an acceptance
  rule, and a log of every decision ([`src/improvement_loop.py`](src/improvement_loop.py)).
- **CLI and Streamlit app:** both call the same `Pipeline.search`.
- **Optional dense / hybrid retrieval:** sentence-transformers embeddings and reciprocal-rank
  fusion are implemented behind an optional extra. They are **not evaluated** and **not used** by
  the baseline or final configuration.

No LLM is used at inference time. Claude Code was used as a development tool (see
[AI-tool usage](#ai-tool-usage)); it isn't part of the retrieval system.

## Setup and installation

Requirements:
- Python **≥ 3.13** (`requires-python` in [`pyproject.toml`](pyproject.toml))
- [uv](https://docs.astral.sh/uv/)
- CPU only; no GPU or API keys

Development and testing were done on Linux; other platforms haven't been tested.

```bash
git clone <repository-url> CIA && cd CIA
uv sync                      # core + dev dependencies, pinned in uv.lock
source .venv/bin/activate    # or prefix commands with `uv run`
uv sync --extra dense        # optional: dense/hybrid dependencies (CPU PyTorch, large download)
```

The alternative with pip is `pip install -r requirements.txt`. That file is exported from
`uv.lock`, includes the optional dense extra, and points pip at the CPU PyTorch index.

**Environment variables:** none are required. `CIA_CONFIG` optionally selects the config used by
the Streamlit app (default `configs/final.yaml`).

## Data preparation

1. Download the public **LegalBench-RAG** dataset to any location. Only
   `benchmarks/cuad.json` and `corpus/cuad/` are used. CUAD is CC BY 4.0 and the LegalBench-RAG
   queries are MIT, as stated in the dataset's `LICENSE` file; follow those terms.
2. Copy the needed files into the repository. Only the contracts referenced by the selected
   queries are copied and indexed; files are byte-copied, checked against the dataset's
   `SHA256SUMS`, and re-running is safe.
   ```bash
   python -m src.cli prepare-data --source /path/to/legalbench-rag
   ```
3. Validate:
   ```bash
   python -m src.cli validate-data
   ```

Raw and processed data (`data/raw/`, `data/processed/`) are gitignored. The frozen unanswerable
set, [`data/unanswerable_queries.json`](data/unanswerable_queries.json), is committed.

`validate-data` prints a JSON report and ends with `VALIDATION OK`. The expected properties are:

| Property | Expected |
|---|---|
| benchmark queries (`n_queries`) | 194 (140 train / 54 test) |
| indexed contracts | 29, equal to the referenced set |
| gold spans | 272, with 0 mismatches against the source text |
| unanswerable queries | 35 (28 train / 7 test), with no absence-term hits |
| chunk offset violations | 0 |

The `n_chunks` value comes from the config passed with `--config`. The default is
`configs/baseline.yaml`, which gives 1,617 chunks; other configs give different counts.

## Usage

Run all commands from the repository root. The examples use `configs/final.yaml` unless stated.

```bash
# A question that names its contract (CUAD style)
python -m src.cli search \
  --query "Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; What is the governing law for this contract?" \
  --top-k 5

# Select the contract explicitly (document ID or a unique substring of it)
python -m src.cli search \
  --query "What is the governing law for this contract?" \
  --document PapaJohns --top-k 5

# An unanswerable question: the system abstains
python -m src.cli search \
  --query "Who won the FIFA World Cup in 2018?" \
  --top-k 5

# JSON output
python -m src.cli search \
  --query "Who won the FIFA World Cup in 2018?" \
  --top-k 5 --json

# Use the baseline configuration
python -m src.cli search \
  --query "What is the governing law for this contract?" \
  --top-k 5 --config configs/baseline.yaml

# Print an exact source span (to check offsets)
python -m src.cli show-span --document PapaJohns --start 63649 --end 63806

# Web app (http://localhost:8501); restart it after editing a config
streamlit run app.py
CIA_CONFIG=configs/baseline.yaml streamlit run app.py

# Help
python -m src.cli --help
python -m src.cli search --help
```

**What you get back.** Each answer states whether the system *answered* or *abstained*, with the
evidence score and threshold, followed by ranked passages: rank, score, document ID,
`[start, end)` offsets and verbatim text.

**Name or select the contract.** With the final configuration, a question that doesn't name a
contract abstains with reason `contract_not_identified` and lists the three closest contracts. If
the contract is ambiguous, name it in the question or select it with `--document` (or with the
sidebar *Contract* selector in the app).

## CLI command reference

| Subcommand | Main arguments | Purpose |
|---|---|---|
| `prepare-data` | `--source DIR` | copy `cuad.json` and the referenced contracts into `data/raw/`; write `data/processed/` |
| `validate-data` | `--config` | validate selection, split, gold spans, unanswerable set and chunk offsets |
| `build-index` | `--config` | chunk and index; write `artifacts/index/<fingerprint>/{chunks.jsonl,stats.json}` |
| `search` | `--query`, `--top-k`, `--document`, `--json`, `--config` | query the pipeline |
| `show-span` | `--document`, `--start`, `--end`, `--config` | print `document[start:end]` from the source text |
| `evaluate` | `--config`, `--split {train,test}`, `--final-test`, `--no-calibrate`, `--write-threshold`, `--out` | per-query and aggregate metrics |
| `improve` | `--config`, `--spec`, `--run-name`, `--max-iterations` | the train-only improvement loop |
| `error-analysis` | `--config`, `--out`, `--per-category` | categorised failures on the train split |
| `demo-check` | `--config`, `--top-k`, `--n-types` | PASS/FAIL battery: train queries, train negatives, unusual inputs |

## Architecture

```
src/data.py            cuad.json -> mini() -> SHA-256 split; load referenced contracts (unmodified)
src/chunking.py        boundary-aware chunks with exact [start, end) offsets
src/text.py            search-only tokenisation; "Consider <preamble>; <question>" parsing
src/retrieval.py       BM25, contract routing, ranking, overlap handling, evidence signals
src/abstention.py      abstention rule and train-only threshold calibration
src/pipeline.py        Pipeline.search: shared by the CLI, the app and evaluation
src/metrics.py         character-level precision/recall/F1@k; abstention metrics
src/evaluation.py      per-query and aggregate results; test-run log
src/diagnostics.py     failure categories and error-analysis output
src/improvement_loop.py  train-only candidate evaluation and acceptance
src/demo_check.py      demo battery
src/cli.py, app.py     CLI and Streamlit front ends
```

Flow for one query in the final configuration:

```
query ─► parse "Consider <preamble>; <question>"
        ─► route: preamble ─► one contract     (or --document; no contract named ─► abstain + suggestions)
        ─► rank: question ─► BM25 over that contract's chunks
        ─► overlap handling: overlapping same-contract passages trimmed to their uncovered part
        ─► abstain? full-query evidence score < calibrated threshold
        ─► output: ranked passages with exact source offsets, or an abstention
```

## Configuration

| File | Role |
|---|---|
| [`configs/baseline.yaml`](configs/baseline.yaml) | initial BM25 configuration: full-query ranking over all contracts; threshold stored after train calibration |
| [`configs/final.yaml`](configs/final.yaml) | configuration selected by the train-only loop and promoted from `artifacts/loop/run3/accepted_config.yaml`, plus `query.require_contract: true` (see REPORT.md) |
| [`configs/loop.yaml`](configs/loop.yaml) | loop protocol (primary metric, guardrails, tolerances) and candidate list, with a change log |

All keys and their defaults are in [`src/config.py`](src/config.py) (`DEFAULTS`). Read the YAML
files for current values.

## Reproduction runbook

### A. Fresh reproduction (train only; recommended order)

This is the recommended workflow for a fresh run. It isn't a record of the order in which the
original experiments happened; see REPORT.md §10 for that.

```bash
uv sync && source .venv/bin/activate
python -m src.cli prepare-data --source /path/to/legalbench-rag
python -m src.cli validate-data                                   # expect VALIDATION OK
python -m pytest -q
python -m src.cli evaluate --config configs/baseline.yaml         # baseline, train split
python -m src.cli improve --config configs/baseline.yaml --spec configs/loop.yaml --run-name <new-name>
#   -> artifacts/loop/<new-name>/{loop.log,iterations.jsonl,accepted_config.yaml,summary.json}
#   promote: copy accepted_config.yaml to a config file; set status: final; add
#   query.require_contract: true to match configs/final.yaml
python -m src.cli evaluate --config configs/final.yaml --no-calibrate   # final, train split
python -m src.cli error-analysis --config configs/final.yaml            # train split
python -m src.cli demo-check --config configs/final.yaml
streamlit run app.py
```

Notes:
- In a fresh run, freeze and commit `data/unanswerable_queries.json` before starting the loop.
- Use a new `--run-name`; reusing one overwrites that directory.
- Train evaluations re-calibrate the abstention threshold unless you pass `--no-calibrate`.

### B. Inspect the existing evaluation artifacts (no new test run)

The reported baseline and final test metrics are already saved. Inspect them without rerunning:

```bash
cat artifacts/test_runs.jsonl                                       # every recorded test evaluation
cat artifacts/eval/overlap_up_test_20261102-153405/metrics_by_k.csv # final, test split
cat artifacts/eval/baseline_test_20261102-153427/metrics_by_k.csv   # baseline, test split
python -m json.tool artifacts/eval/overlap_up_test_20261102-153405/metrics.json | head -60
cat artifacts/loop/run3/summary.json                                # loop run that selected the final config
```

### C. New test evaluation (only for a newly frozen configuration)

> **Warning:** this runs the held-out test split and appends a record to
> `artifacts/test_runs.jsonl`. Test results must not be used to tune or select configurations.
> You don't need it to inspect the existing results (section B).

```bash
python -m src.cli evaluate --config configs/final.yaml --split test --final-test
```

The CLI refuses to evaluate the test split without `--final-test`, and it never re-calibrates
the threshold on test.

## Testing

```bash
python -m pytest -q          # most recent run reported by the author: 83 passed
```

| File | Covers |
|---|---|
| `tests/test_metrics.py` | exact/partial coverage, extra text, wrong document, multiple gold spans, overlapping passages, empty retrieval, k cutoffs, aggregation, abstention-metric denominators |
| `tests/test_data.py` | `mini()` determinism, split, gold-span validation, negative-set contract, idempotent data preparation |
| `tests/test_chunking.py` | offset invariants, overlap behaviour, boundary preference |
| `tests/test_retrieval.py` | BM25 against a hand-computed score, ranking/ties, top-k, routing, overlap policies, contract identity, document filter, dense/hybrid paths with a stub encoder |
| `tests/test_abstention.py` | threshold equality, calibration, single- and two-threshold rules, false abstention and failure to abstain |
| `tests/test_improvement_loop.py` | one-command run, train-only data, logging, rejected candidates never overwrite the accepted config, frozen-set integrity, reproducibility |
| `tests/test_end_to_end.py` | CLI, headless Streamlit (`AppTest`), invalid config, evaluation outputs, test-split refusal, `show-span`, `demo-check` |

Most tests use small synthetic fixtures (`tests/conftest.py`). Tests marked `real_data` need the
prepared benchmark under `data/raw/` and are skipped otherwise.

`demo-check` is a separate manual battery. With `configs/final.yaml` the author's most recent
run gave:
- **A answerable: 4/10.** The six failures are 5 wrong-passage results and 1 false abstention;
  these are genuine retrieval errors.
- **B unanswerable: 4/4**
- **C input handling: 13/13**

## Assumptions and limitations

- **Query format.** Contract routing expects a CUAD-style "Consider …;" preamble. Free-form
  references to a contract aren't resolved.
- **Single-contract routing.** Each query is routed to one contract. A wrong routing decision
  means no correct evidence can be returned.
- **Low precision.** Returned passages are much longer than typical gold spans, so most of the
  returned text isn't the answer.
- **Lexical matching.** Paraphrased clauses with different vocabulary can be missed.
- **Dense/hybrid retrieval** is implemented but not evaluated.
- **The unanswerable set** is hand-authored (35 queries), and only 7 fall in the test split, so
  evidence about abstention is limited.
- **Small benchmark.** 29 contracts, shared between train and test.
- **Offsets** are Python string indices into the file as read by
  `open(path, encoding="utf-8").read()` (default text mode, universal newlines).
- **Retrieval isn't legal relevance.** A returned passage isn't a legal conclusion, an abstention
  doesn't prove a clause is absent, and scores aren't probabilities. This isn't legal advice.

## AI-tool usage

- **Tool:** this project was developed with **Claude Code** (Anthropic) as an AI coding
  assistant.
- **AI-assisted:** most of the source code, tests, configurations, the unanswerable-query set and
  drafts of the documentation were generated with the assistant, at the developer's direction.
- **Run by the developer locally:** dependency installation, data preparation, test runs, train
  and test evaluations, and all improvement-loop runs. The outputs were reviewed with the
  assistant.
- **Corrections during development:** some AI-suggested example queries were wrong; the
  developer caught them, and they were replaced with verified ones. Design changes (question-only
  ranking with full-query abstention, contract-identity abstention) came from reviewing
  train-split diagnostics.
- **Responsibility:** the developer reviewed the implementation and is responsible for it.
- **No runtime LLM:** an LLM is not part of the retrieval system.

## Report

The evaluation setup, baseline-versus-final results, iteration history, error analysis,
limitations and the test-evaluation history are in **[REPORT.md](REPORT.md)**.
