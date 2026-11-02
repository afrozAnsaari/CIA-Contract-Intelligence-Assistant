import json
import random

from src.config import load_config
from src.data import (assign_split, load_dataset, load_unanswerable, mini, prepare_data, read_source,
                      referenced_documents, validate_dataset)
from tests.conftest import real_data, write_tiny_raw


def _fake_tests(n):
    return [{"query": f"q{i}", "snippets": [{"file_path": f"cuad/doc{i % 37}.txt", "span": [0, 1], "answer": "x"}]}
            for i in range(n)]


def test_mini_deterministic_and_size():
    t = _fake_tests(500)
    a, b = mini(t), mini(list(reversed(t)))
    assert len(a) == 194
    assert [x["snippets"][0]["file_path"] for x in a] == [x["snippets"][0]["file_path"] for x in b]
    assert mini(t[:50]) == t[:50]


def test_mini_matches_reference_logic():
    t = _fake_tests(300)

    def key(x):
        random.seed(x["snippets"][0]["file_path"])
        return random.random()
    assert mini(t) == sorted(t, key=key)[:194]


def test_split_deterministic_and_partition():
    qs = [f"query number {i}" for i in range(200)]
    s1 = [assign_split(q) for q in qs]
    assert s1 == [assign_split(q) for q in qs]
    assert set(s1) == {"train", "test"}
    assert assign_split("  hello ") == assign_split("hello")  # strip() per protocol


def test_dataset_gold_and_documents(tiny):
    cfg, ds = tiny
    rep = validate_dataset(ds)
    assert rep["gold_spans_mismatched"] == 0
    assert rep["indexed_equals_referenced"]
    assert rep["split_partition_ok"]
    assert rep["ok"], rep
    for q in ds.queries:
        assert len([s for s in ("train", "test") if q in ds.split(s)]) == 1


def test_gold_mismatch_detected(tiny):
    cfg, ds = tiny
    doc = next(iter(ds.documents))
    ds.documents[doc] = "X" + ds.documents[doc]
    assert validate_dataset(ds)["gold_spans_mismatched"] > 0


def test_read_source_does_not_alter_text(tmp_path):
    p = tmp_path / "a.txt"
    p.write_bytes("café  \n\n  x\t".encode("utf-8"))
    assert read_source(p) == "café  \n\n  x\t"


def test_negative_set_contract(tiny):
    cfg, ds = tiny
    negs = load_unanswerable(cfg)
    assert len(negs) >= 30 and len({n.qid for n in negs}) == len(negs)
    assert all(not n.answerable and n.split == assign_split(n.query) for n in negs)


def test_prepare_data_idempotent(tmp_path):
    src = tmp_path / "src"
    write_tiny_raw(src)
    cfg = load_config(None, {"data.raw_dir": str(tmp_path / "raw"), "data.processed_dir": str(tmp_path / "proc")})
    m1 = prepare_data(src, cfg)
    m2 = prepare_data(src, cfg)
    assert m1["files_copied"] == 3 and m2["files_copied"] == 0 and m2["files_unchanged"] == 3
    assert (tmp_path / "raw" / "corpus" / "cuad" / "AlphaCo_License Agreement.txt").read_bytes() == \
        (src / "corpus" / "cuad" / "AlphaCo_License Agreement.txt").read_bytes()


@real_data
def test_real_mini_selection_and_validation():
    cfg = load_config("configs/baseline.yaml")
    ds = load_dataset(cfg)
    rep = validate_dataset(ds)
    assert rep["n_queries"] == 194
    assert rep["ok"], rep
    tests = json.loads(read_source(__import__("src.config", fromlist=["x"]).resolve_path(
        cfg["data"]["raw_dir"]) / "benchmarks" / "cuad.json"))["tests"]
    assert set(ds.documents) == set(referenced_documents(mini(tests)))


@real_data
def test_committed_negative_set_is_valid():
    cfg = load_config("configs/baseline.yaml")
    negs = load_unanswerable(cfg)
    assert len(negs) >= 30
    assert all(n.rationale and n.category for n in negs)
