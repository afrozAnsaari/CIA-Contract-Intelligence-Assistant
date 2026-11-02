"""Manual acceptance check: a fixed, deterministic battery of cases run through the SAME
`Pipeline.search` used by the CLI and the web app, with PASS/FAIL judged automatically.

Uses TRAIN data only (benchmark train queries + train part of the unanswerable set), so it
never inspects the held-out test split. Case selection is deterministic (no cherry-picking):
  A. answerable  - for each of the most frequent question types, the first train query
                   (by qid) of that type. PASS = answered AND a top-k passage overlaps gold.
  B. unanswerable - the first train negative (by id) of every category. PASS = abstained.
  C. input handling - empty/whitespace/invalid top-k must give a clean error; odd but
                   valid inputs must not crash and must return exact source offsets.
A and B measure retrieval quality (some failures are expected and are real system errors);
C measures robustness (any failure is a bug).
"""

from __future__ import annotations

from collections import OrderedDict

from .data import load_dataset
from .pipeline import Pipeline, PipelineError
from .text import split_query


def _overlaps_gold(passages: list[dict], gold) -> bool:
    return any(p["document_id"] == g.document_id and p["start_offset"] < g.end and g.start < p["end_offset"]
               for p in passages for g in gold)


def _offsets_exact(pipe: Pipeline, passages: list[dict]) -> bool:
    return all(pipe.documents[p["document_id"]][p["start_offset"]:p["end_offset"]] == p["text"] for p in passages)


def answerable_cases(ds, n_types: int) -> list:
    by_type: dict[str, list] = OrderedDict()
    for q in sorted(ds.split("train"), key=lambda q: q.qid):
        by_type.setdefault(split_query(q.query)[1], []).append(q)
    types = sorted(by_type, key=lambda t: (-len(by_type[t]), t))[:n_types]
    return [by_type[t][0] for t in types]


def unanswerable_cases(ds) -> list:
    seen, out = set(), []
    for n in sorted(ds.split("train", answerable=False), key=lambda n: n.qid):
        if n.category not in seen:
            seen.add(n.category)
            out.append(n)
    return out


def run_demo_check(pipe: Pipeline, top_k: int = 5, n_types: int = 10) -> dict:
    ds = load_dataset(pipe.cfg)
    rows = []

    for q in answerable_cases(ds, n_types):
        r = pipe.search(q.query, top_k)
        hit = (not r.abstained) and _overlaps_gold(r.passages, q.gold)
        why = "abstained (false abstention)" if r.abstained else ("gold in top-k" if hit else "answered, wrong passages")
        rows.append(("A answerable", q.query, "answer + gold in top-k", why, hit, r.signal_text()))

    for n in unanswerable_cases(ds):
        r = pipe.search(n.query, top_k)
        rows.append((f"B unanswerable/{n.category}", n.query, "abstain",
                     "abstained" if r.abstained else f"answered {len(r.passages)} (failure to abstain)",
                     r.abstained, r.signal_text()))

    def expect_error(label, query, k):
        try:
            pipe.search(query, k)
            rows.append(("C input", label, "clean error", "no error raised", False, ""))
        except PipelineError as e:
            rows.append(("C input", label, "clean error", f"error: {e}", True, ""))

    def expect_ok(label, query, k=top_k):
        try:
            r = pipe.search(query, k)
            ok = _offsets_exact(pipe, r.passages) and len(r.passages) <= k
            got = "abstained" if r.abstained else f"answered {len(r.passages)}"
            rows.append(("C input", label, "no crash, exact offsets, <= k", got, ok, r.signal_text()))
        except Exception as e:  # any exception here is a robustness bug
            rows.append(("C input", label, "no crash, exact offsets, <= k", f"CRASH {type(e).__name__}: {e}", False, ""))

    expect_error("empty query ''", "", top_k)
    expect_error("whitespace query '   '", "   ", top_k)
    expect_error("top_k = 0", "governing law", 0)
    expect_ok("top_k = 1", ds.split("train")[0].query, 1)
    expect_ok("top_k = 50 (large)", ds.split("train")[0].query, 50)
    r = pipe.search("the of and", top_k)
    rows.append(("C input", "stopwords only 'the of and'", "abstain (no content terms)",
                 r.abstention_reason, r.abstained and r.abstention_reason == "no_candidates", ""))
    expect_ok("punctuation only '?!;'", "?!;")
    expect_ok("SQL-like text", "'; DROP TABLE contracts; --")
    expect_ok("non-English (Hindi)", "इस अनुबंध का शासी कानून क्या है?")
    expect_ok("emoji", "📄🤔 governing law?")
    expect_ok("very long query (5k chars)", "governing law " * 360)
    if pipe.cfg["query"]["mode"] == "split" and pipe.cfg["query"].get("require_contract"):
        r = pipe.search("What is the governing law for this contract?", top_k)
        rows.append(("C input", "no contract named (require_contract)", "abstain: contract_not_identified",
                     f"{r.abstention_reason}; suggestions={len(r.contract_candidates)}",
                     r.abstained and r.abstention_reason == "contract_not_identified" and not r.passages, ""))
        doc = sorted(pipe.documents)[0]
        r = pipe.search("What is the governing law for this contract?", top_k, document=doc)
        rows.append(("C input", "document filter keeps results in that contract", "all passages from it",
                     f"{len(r.passages)} passages", all(p["document_id"] == doc for p in r.passages), r.signal_text()))
    else:
        expect_ok("no 'Consider ...;' preamble", "What is the governing law for this contract?")

    summary = {}
    for grp in ("A", "B", "C"):
        g = [r for r in rows if r[0].startswith(grp)]
        summary[grp] = (sum(r[4] for r in g), len(g))
    return {"rows": rows, "summary": summary, "config": pipe.cfg.get("name"), "status": pipe.cfg.get("status")}


def format_report(res: dict, width: int = 95) -> str:
    out = [f"demo-check  config={res['config']} ({res['status']})", ""]
    for grp, label, exp, got, ok, sig in res["rows"]:
        q = label if len(label) <= width else label[: width - 3] + "..."
        out.append(f"[{'PASS' if ok else 'FAIL'}] {grp}: {q}")
        out.append(f"        expected: {exp} | got: {got}" + (f" | {sig}" if sig else ""))
    s = res["summary"]
    out += ["", f"A answerable (train) : {s['A'][0]}/{s['A'][1]} pass   <- retrieval quality; failures are real system errors",
            f"B unanswerable (train): {s['B'][0]}/{s['B'][1]} pass   <- abstention quality",
            f"C input handling      : {s['C'][0]}/{s['C'][1]} pass   <- robustness; any FAIL here is a bug"]
    return "\n".join(out)
