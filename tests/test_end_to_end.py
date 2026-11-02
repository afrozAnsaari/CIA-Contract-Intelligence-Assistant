import json
import subprocess
import sys

import pytest
import yaml

from src import cli
from src.config import REPO_ROOT
from src.evaluation import evaluate, write_results
from src.pipeline import Pipeline
from tests.conftest import real_data


def _write_cfg(cfg, tmp_path):
    p = tmp_path / "cfg.yaml"
    p.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return str(p)


def test_answerable_query_end_to_end(tiny):
    cfg, ds = tiny
    r = Pipeline(cfg, ds.documents).search(
        "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What is the governing law for this contract?", 3)
    assert not r.abstained
    assert any("governed by the laws" in p["text"] for p in r.passages)
    assert set(r.passages[0]) >= {"document_id", "start_offset", "end_offset", "text", "score", "rank"}


def test_unanswerable_query_end_to_end(tiny):
    cfg, ds = tiny
    r = Pipeline(cfg, ds.documents).search("What does the agreement say about quintessor obligations?", 5)
    assert r.abstained and r.passages == []


def test_cli_search(tiny, tmp_path, capsys):
    cfg, _ = tiny
    path = _write_cfg(cfg, tmp_path)
    rc = cli.main(["search", "--query", "What restrictions apply to sublicensing?", "--top-k", "2",
                   "--config", path, "--json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert len(out["passages"]) <= 2 and "abstained" in out
    assert cli.main(["search", "--query", "  ", "--config", path]) == 2


def test_cli_and_web_use_same_pipeline(tiny, tmp_path, capsys):
    import app
    cfg, ds = tiny
    q = "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; What are the insurance requirements?"
    web = app.run_query(Pipeline(cfg, ds.documents), q, 3).to_dict()
    cli.main(["search", "--query", q, "--top-k", "3", "--config", _write_cfg(cfg, tmp_path), "--json"])
    assert json.loads(capsys.readouterr().out) == web


def test_cli_refuses_test_split_without_flag(tiny, tmp_path):
    cfg, _ = tiny
    assert cli.main(["evaluate", "--split", "test", "--config", _write_cfg(cfg, tmp_path)]) == 2
    with pytest.raises(PermissionError):
        evaluate(cfg, tiny[1], "test")


def test_evaluation_writes_files(tiny, tmp_path):
    cfg, ds = tiny
    out = write_results(evaluate(cfg, ds, "train"), tmp_path / "ev")
    for f in ("per_query.jsonl", "metrics.json", "metrics_by_k.csv", "config_used.yaml"):
        assert (out / f).exists()
    m = json.loads((out / "metrics.json").read_text())
    assert m["retrieval"]["n"] == len(ds.split("train")) and m["offset_errors"] == 0
    assert m["calibration"]["n_neg"] <= len(ds.split("train", False))


def test_cli_evaluate_and_test_run_counter(tiny, tmp_path, capsys):
    cfg, _ = tiny
    path = _write_cfg(cfg, tmp_path)
    assert cli.main(["evaluate", "--config", path, "--out", str(tmp_path / "tr")]) == 0
    assert cli.main(["evaluate", "--config", path, "--split", "test", "--final-test", "--out", str(tmp_path / "te")]) == 0
    log = tmp_path / "artifacts" / "test_runs.jsonl"
    assert len(log.read_text().splitlines()) == 1


def test_streamlit_app_handles_query(tiny, tmp_path, monkeypatch):
    pytest.importorskip("streamlit.testing.v1")
    from streamlit.testing.v1 import AppTest
    cfg, _ = tiny
    monkeypatch.setenv("CIA_CONFIG", _write_cfg(cfg, tmp_path))
    at = AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception
    at.text_area[0].input("Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What is the governing law?")
    at.button[0].click().run()
    assert not at.exception
    assert any("passage" in s.value for s in at.success) or at.warning


def test_cli_help_runs():
    r = subprocess.run([sys.executable, "-m", "src.cli", "search", "--help"], capture_output=True, text=True)
    assert r.returncode == 0 and "--top-k" in r.stdout


@real_data
def test_real_search_smoke():
    r = Pipeline.from_config("configs/baseline.yaml").search("What is the governing law for this contract?", 3)
    assert r.passages or r.abstained


def test_demo_check_runs(tiny):
    from src.demo_check import format_report, run_demo_check
    cfg, ds = tiny
    res = run_demo_check(Pipeline(cfg, ds.documents), top_k=3, n_types=3)
    assert res["summary"]["C"][0] == res["summary"]["C"][1]  # input handling must be robust
    assert res["summary"]["A"][1] >= 1 and res["summary"]["B"][1] >= 1
    assert "PASS" in format_report(res)


def test_cli_show_span_and_document_option(tiny, tmp_path, capsys):
    cfg, ds = tiny
    path = _write_cfg(cfg, tmp_path)
    doc = "cuad/AlphaCo_License Agreement.txt"
    s = ds.documents[doc].index("governed by")
    assert cli.main(["show-span", "--document", "AlphaCo", "--start", str(s), "--end", str(s + 11),
                     "--config", path]) == 0
    assert capsys.readouterr().out.strip().endswith("governed by")
    assert cli.main(["show-span", "--document", "AlphaCo", "--start", "5", "--end", "999999", "--config", path]) == 2
    assert cli.main(["search", "--query", "governing law", "--document", "AlphaCo", "--config", path, "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert all(p["document_id"] == doc for p in out["passages"])


def test_streamlit_invalid_config_is_controlled(monkeypatch):
    pytest.importorskip("streamlit.testing.v1")
    from streamlit.testing.v1 import AppTest
    monkeypatch.setenv("CIA_CONFIG", "does/not/exist.yaml")
    at = AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception          # no unhandled traceback
    assert at.error                  # a controlled error message is shown


@real_data
def test_real_document_filter_papajohns_governing_law():
    p = Pipeline.from_config("configs/final.yaml")
    r = p.search("What is the governing law for this contract?", 5, document="PapaJohns")
    assert r.passages, "known answerable contract/question must return passages"
    assert all("PapaJohns" in x["document_id"] for x in r.passages)
    assert any("Delaware" in x["text"] for x in r.passages)


# Train-split regression cases from the six-failure audit (never test-split queries).
FIXED_BY_QUERY_REFINEMENT = ["cuad-0f789ebcf3", "cuad-05251665f3", "cuad-3fdb534e55", "cuad-5fce387d80"]


def _gold_rank(pipe, q):
    out = pipe.retrieve(q.query, 64)
    return next((x.rank for x in out.passages if any(
        x.document_id == g.document_id and x.start_offset < g.end and g.start < x.end_offset for g in q.gold)), None)


@real_data
@pytest.mark.parametrize("qid", FIXED_BY_QUERY_REFINEMENT)
def test_real_query_refinement_fixes_audited_failures(qid):
    from src.data import load_dataset
    p = Pipeline.from_config("configs/candidate_v4.yaml")
    q = next(q for q in load_dataset(p.cfg).queries if q.qid == qid)
    assert q.split == "train"
    r = p.search(q.query, 5)
    assert not r.abstained and _gold_rank(p, q) <= 5
    for x in r.passages:  # offsets stay exact
        assert p.documents[x["document_id"]][x["start_offset"]:x["end_offset"]] == x["text"]


@real_data
@pytest.mark.xfail(strict=True, reason="known limitation: BicycleTX IP (E1) false abstention; lexical "
                   "signals score its unanswerable counterpart unans-025 higher (REPORT §11)")
def test_real_bicycletx_ip_is_answered():
    p = Pipeline.from_config("configs/candidate_v4.yaml")
    r = p.search("Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business "
                 "Officer Position; How is intellectual property ownership assigned in this contract?", 5)
    assert not r.abstained
