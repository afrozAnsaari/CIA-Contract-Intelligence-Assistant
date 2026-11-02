# Manual runbook (commands to execute locally)

All commands run from the repository root (`/home/afrozdebian/coding/JioStar/CIA`) with the venv
active (`source .venv/bin/activate`), or prefix each with `uv run`. Timings are estimates unless noted.

| # | Step | Command | Expected output / artifacts | Success check | Cost |
|---|------|---------|-----------------------------|---------------|------|
| 1 | Install core + dev deps | `uv sync` | `.venv/` | `python -c "import streamlit, numpy, yaml, snowballstemmer"` exits 0 | ~1 min, network |
| 1b | *(optional)* dense/hybrid extra | `uv sync --extra dense` | CPU torch + sentence-transformers in `.venv` | `python -c "import sentence_transformers"` | ~1-3 GB download, several min |
| 2 | Copy benchmark + the 29 referenced contracts | `python -m src.cli prepare-data --source /home/afrozdebian/coding/datasets/legalbench-rag` | `data/raw/legalbench-rag/{benchmarks/cuad.json,corpus/cuad/*.txt}`, `data/processed/manifest.json`, `data/processed/cuad_mini_queries.jsonl` | prints `mini_n: 194`, `n_documents: 29`, `train: 140`, `test: 54`, `checksums_verified: 30`, `OK: data prepared` | seconds |
| 3 | Validate data | `python -m src.cli validate-data` | JSON report | `gold_spans_mismatched: 0`, `indexed_equals_referenced: true`, `n_unanswerable: 35` (28 train / 7 test), `unanswerable_absence_term_hits: {}`, `chunk_offset_violations: 0`, last line `VALIDATION OK` | seconds |
| 4 | Freeze the negative set (before any loop run) | `git add data/unanswerable_queries.json && git commit -m "Freeze unanswerable query set v1.0"` | commit | `git log -1 -- data/unanswerable_queries.json` shows the commit; never edit the file afterwards | - |
| 5 | Full test suite | `python -m pytest -q` | - | `77 passed` (real-data tests skip if step 2 not done) | seconds |
| 6 | Build index + stats | `python -m src.cli build-index --config configs/baseline.yaml` | `artifacts/index/<fingerprint>/{chunks.jsonl,stats.json}` | `n_documents: 29`, `n_chunks: 1617` for baseline | seconds (BM25 only; dense configs embed and cache `dense_embeddings.npy`, minutes on CPU) |
| 7 | Baseline TRAIN eval | `python -m src.cli evaluate --config configs/baseline.yaml --split train` | `artifacts/eval/baseline_train_<ts>/{metrics.json,metrics_by_k.csv,per_query.jsonl,config_used.yaml}` | table of P/R/F1 at k=1..64, `answerable n=140 unanswerable n=28 offset_errors=0`, calibrated threshold line | seconds |
| 8 | Improvement loop (TRAIN only) | `python -m src.cli improve --config configs/baseline.yaml --spec configs/loop.yaml` | `artifacts/loop/<ts>/{loop.log,iterations.jsonl,accepted_config.yaml,summary.json,iterNN_<id>/...}` | ends with `[loop] done. evaluated=N accepted=<id>`, N >= 5, exit code 0. Follow live: `tail -f artifacts/loop/<ts>/loop.log` | ~1-2 min BM25-only (dense candidates are skipped unless step 1b done; then add several min) |
| 9 | Inspect decisions | `python -c "import json;[print(r['candidate_id'],r['decision'],r.get('primary_delta'),r['reason']) for r in map(json.loads,open('artifacts/loop/<ts>/iterations.jsonl'))]"` and `cat artifacts/loop/<ts>/accepted_config.yaml` | - | every candidate has a decision + reason; accepted config is the last `accepted` row | - |
| 10a | Promote final config | `cp artifacts/loop/<ts>/accepted_config.yaml configs/final.yaml`, then edit `status: final` (and `name:` if desired) | `configs/final.yaml` (contains the train-calibrated threshold) | `python -m src.cli build-index --config configs/final.yaml` works | - |
| 10b | **Final TEST eval (once)** | `python -m src.cli evaluate --config configs/final.yaml --split test --final-test` | `artifacts/eval/<name>_test_<ts>/...`, appends to `artifacts/test_runs.jsonl` | prints `[test-run #1 recorded ...]`, `answerable n=54 unanswerable n=7`; threshold line says "(from config)" (never re-calibrated on test) | seconds |
| 10c | Baseline on TEST (for the report's baseline-vs-final table) | first `python -m src.cli evaluate --config configs/baseline.yaml --write-threshold` (stores the train threshold), then `python -m src.cli evaluate --config configs/baseline.yaml --split test --final-test` | as above | test-run #2 recorded | seconds |
| 11 | Error analysis (TRAIN) | `python -m src.cli error-analysis --config configs/baseline.yaml` and `python -m src.cli error-analysis --config configs/final.yaml` | `artifacts/error_analysis/<name>/{error_analysis.md,failures.jsonl,summary.json}` | `n_failures` >= 10 across the two; categories grouped in the .md | seconds |
| 12 | Demo | `streamlit run app.py` (uses `configs/final.yaml`; override with `CIA_CONFIG=configs/baseline.yaml streamlit run app.py`) | browser at http://localhost:8501 | answerable query shows ranked passages with doc id + offsets; nonsense query shows "Abstained" | - |
| 12b | CLI examples | `python -m src.cli search \`<br>`  --query "Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; What is the governing law for this contract?" \`<br>`  --top-k 5`<br><br>`python -m src.cli search \`<br>`  --query "Who won the FIFA World Cup in 2018?" \`<br>`  --top-k 5` | stdout | first: `Answered with N passage(s)`; second: `ABSTAINED` (once a calibrated threshold is in the config) | seconds |
| 13 | Final checks | `python -m pytest -q`; `git status`; `git ls-files \| xargs du -ch \| tail -1` | - | all pass; no `data/raw`, `artifacts/index`, `.env`, PDF or `prompt.md` tracked | - |

Notes
- `configs/final.yaml` is **provisional** (= baseline, threshold 0.0, so it only abstains when nothing
  matches) until step 10a. Before demoing on it, run `python -m src.cli evaluate --config configs/final.yaml --write-threshold`.
- The test split cannot be evaluated without `--final-test`; each test run is counted in `artifacts/test_runs.jsonl`.
- Regenerate `requirements.txt` after dependency changes:
  `uv export --no-hashes --all-extras --all-groups -o requirements.txt && sed -i '1i --extra-index-url https://download.pytorch.org/whl/cpu' requirements.txt`
