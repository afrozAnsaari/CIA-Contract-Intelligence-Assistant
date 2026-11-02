"""Shared fixtures: a tiny synthetic LegalBench-RAG-shaped dataset in a temp directory."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.config import REPO_ROOT, load_config
from src.data import assign_split, load_dataset

DOC_A = (
    "LICENSE AGREEMENT\n\nThis License Agreement is made between AlphaCo Inc. (Licensor) and Gamma LLC (Licensee).\n\n"
    "1. Grant. Licensor grants Licensee a non-exclusive license to use the Licensed Technology.\n\n"
    "2. Sublicensing. Licensee shall not sublicense the Licensed Technology to any third party without the "
    "prior written consent of Licensor.\n\n"
    "3. Governing Law. This Agreement shall be governed by the laws of the State of New York.\n\n"
    "4. Term. This Agreement expires on December 31, 2030 unless terminated earlier.\n"
)
DOC_B = (
    "SUPPLY AGREEMENT\n\nThis Supply Agreement is entered into by BetaInc Corp. (Supplier) and Delta Stores (Buyer).\n\n"
    "1. Minimum Purchase. Buyer shall purchase a minimum of 10,000 units of Product in each calendar year.\n\n"
    "2. Termination for Convenience. Either party may terminate this Agreement for convenience upon ninety (90) "
    "days prior written notice.\n\n"
    "3. Insurance. Supplier shall maintain commercial general liability insurance of at least $1,000,000.\n"
)
DOCS = {"cuad/AlphaCo_License Agreement.txt": DOC_A, "cuad/BetaInc_Supply Agreement.txt": DOC_B}

QA = [
    ("cuad/AlphaCo_License Agreement.txt", "Licensee shall not sublicense the Licensed Technology",
     "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What restrictions apply to sublicensing?"),
    ("cuad/AlphaCo_License Agreement.txt", "This Agreement shall be governed by the laws of the State of New York.",
     "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What is the governing law for this contract?"),
    ("cuad/AlphaCo_License Agreement.txt", "This Agreement expires on December 31, 2030",
     "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What is the expiration date of this contract?"),
    ("cuad/BetaInc_Supply Agreement.txt", "Buyer shall purchase a minimum of 10,000 units of Product in each calendar year.",
     "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; Is there a minimum commitment required?"),
    ("cuad/BetaInc_Supply Agreement.txt", "Either party may terminate this Agreement for convenience upon ninety (90) days prior written notice.",
     "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; Can this contract be terminated for convenience?"),
    ("cuad/BetaInc_Supply Agreement.txt", "Supplier shall maintain commercial general liability insurance of at least $1,000,000.",
     "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; What are the insurance requirements?"),
    ("cuad/BetaInc_Supply Agreement.txt", "Buyer shall purchase a minimum of 10,000 units",
     "Consider the Supply Agreement between BetaInc Corp. and Delta Stores; Does this contract include volume restrictions?"),
    ("cuad/AlphaCo_License Agreement.txt", "Licensor grants Licensee a non-exclusive license to use the Licensed Technology.",
     "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; What licenses are granted under this contract?"),
]

NEG_TOPICS = ["zorblax", "quintessor", "flumbridge", "glarnok", "vexidrome", "snorfle", "trimbulon", "wazzoon",
              "plimbert", "yondric", "krellium", "boopsy", "draxxon", "mimblewort", "quorvex", "slithrak",
              "fendrill", "zibbleton", "orkwad", "hextanol", "jumbrix", "lorpwick", "nexulon", "pibbrow",
              "qaztron", "rumbleflax", "skeevor", "tolquin", "ublaxo", "vornish", "wexlor", "yarbleton"]


def write_tiny_raw(root: Path) -> None:
    tests = []
    for doc, ans, q in QA:
        start = DOCS[doc].index(ans)
        tests.append({"query": q, "snippets": [{"file_path": doc, "span": [start, start + len(ans)], "answer": ans}]})
    # one multi-span query
    a1, a2 = "Licensee shall not sublicense", "governed by the laws of the State of New York"
    d = "cuad/AlphaCo_License Agreement.txt"
    tests.append({"query": "Consider the License Agreement between AlphaCo Inc. and Gamma LLC; Summarise sublicensing and law.",
                  "snippets": [{"file_path": d, "span": [DOCS[d].index(x), DOCS[d].index(x) + len(x)], "answer": x}
                               for x in (a1, a2)]})
    (root / "benchmarks").mkdir(parents=True, exist_ok=True)
    (root / "benchmarks" / "cuad.json").write_text(json.dumps({"tests": tests}), encoding="utf-8")
    for doc, text in DOCS.items():
        p = root / "corpus" / doc
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def write_negatives(path: Path) -> None:
    qs = [{"id": f"unans-{i:03d}", "category": "absent_topic",
           "query": f"What does the agreement say about {t} obligations?",
           "absence_check_terms": [t], "rationale": f"'{t}' is a made-up word absent from the corpus."}
          for i, t in enumerate(NEG_TOPICS, 1)]
    path.write_text(json.dumps({"queries": qs}), encoding="utf-8")


@pytest.fixture()
def tiny(tmp_path):
    raw = tmp_path / "raw"
    write_tiny_raw(raw)
    neg = tmp_path / "unanswerable.json"
    write_negatives(neg)
    cfg = load_config(None, {
        "name": "tiny", "data.raw_dir": str(raw), "data.unanswerable_path": str(neg),
        "data.processed_dir": str(tmp_path / "processed"), "output.artifacts_dir": str(tmp_path / "artifacts"),
        "chunking.max_chars": 200, "chunking.overlap_chars": 30, "retrieval.max_k": 16,
        "evaluation.k_values": [1, 2, 4, 5], "abstention.threshold": 0.05,
    })
    ds = load_dataset(cfg)
    return cfg, ds


REAL_RAW = REPO_ROOT / "data" / "raw" / "legalbench-rag" / "benchmarks" / "cuad.json"
real_data = pytest.mark.skipif(not REAL_RAW.exists(), reason="real data not prepared (run prepare-data)")


def splits_of(queries):
    return {q: assign_split(q) for q in queries}
