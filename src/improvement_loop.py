"""Deterministic, train-only self-improvement loop.

1. Evaluate the baseline config on TRAIN (answerable + unanswerable), calibrating the
   abstention threshold on train only. It becomes the accepted config (iteration 0).
2. Repeat: diagnose failures of the accepted config -> rule-based proposer picks the first
   untried candidate whose `tags` contain the dominant failure category, else the next
   untried candidate in queue order -> apply its changes on top of the ACCEPTED config ->
   evaluate on train -> accept iff primary improves by >= min_improvement and every
   guardrail holds -> log the iteration (accepted or rejected).
Test queries are removed from the dataset object before the loop starts, so no test
label or metric can influence any decision. The frozen negative set is hashed before and
after; a mismatch aborts the run.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import subprocess
import time
from pathlib import Path

import yaml

from .config import apply_overrides, config_fingerprint, dump_config, get_dotted, resolve_path, validate_config
from .data import Dataset, unanswerable_set_hash
from .diagnostics import error_analysis
from .evaluation import evaluate, format_summary, write_results
from .retrieval import dense_available


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _git_rev() -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                              cwd=resolve_path("."), timeout=5).stdout.strip() or None
    except Exception:  # pragma: no cover
        return None


def load_loop_spec(path: str | Path) -> dict:
    with open(resolve_path(path), encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    for key in ("protocol", "candidates"):
        if key not in spec:
            raise ValueError(f"loop spec missing '{key}'")
    ids = [c["id"] for c in spec["candidates"]]
    if len(set(ids)) != len(ids):
        raise ValueError("candidate ids must be unique")
    return spec


def resolve_changes(cfg: dict, changes: dict) -> dict:
    """Values may be literals or {"frac_of": "<dotted key>", "frac": f} (resolved vs cfg)."""
    out = {}
    for k, v in changes.items():
        if isinstance(v, dict) and "frac_of" in v:
            v = int(round(get_dotted(cfg, v["frac_of"]) * float(v["frac"])))
        out[k] = v
    return out


def metric_value(res: dict, dotted: str) -> float | None:
    node = res
    head, _, rest = dotted.partition(".")
    if head not in node:
        return None
    node = node[head]
    if rest:
        if not isinstance(node, dict) or rest not in node:
            return None
        node = node[rest]
    return node


def compare(cand: dict, accepted: dict, protocol: dict) -> tuple[bool, str, list[dict], float | None]:
    """Predeclared acceptance rule. Returns (accept, reason, guardrail_checks, primary_delta)."""
    pm = protocol["primary_metric"]
    c, a = metric_value(cand, pm), metric_value(accepted, pm)
    delta = None if c is None or a is None else c - a
    checks = []
    for g in protocol.get("guardrails", []):
        cv, av = metric_value(cand, g["metric"]), metric_value(accepted, g["metric"])
        ok = True
        rule = ""
        if "must_equal" in g:
            ok = cv == g["must_equal"]
            rule = f"== {g['must_equal']}"
        if "max_drop" in g:
            if cv is None or av is None:
                ok = av is None  # metric unavailable on both sides => vacuous
            else:
                ok = ok and cv >= av - float(g["max_drop"])
            rule = f">= accepted - {g['max_drop']}"
        if "min_value" in g:
            ok = ok and cv is not None and cv >= float(g["min_value"])
            rule = f">= {g['min_value']}"
        checks.append({"metric": g["metric"], "candidate": cv, "accepted": av, "rule": rule, "passed": bool(ok)})
    failed = [x["metric"] for x in checks if not x["passed"]]
    if delta is None:
        return False, f"primary metric {pm} unavailable", checks, delta
    if delta < float(protocol["min_improvement"]):
        return False, f"{pm} delta {delta:+.4f} < min_improvement {protocol['min_improvement']}", checks, delta
    if failed:
        return False, "guardrail(s) failed: " + ", ".join(failed), checks, delta
    return True, f"{pm} improved by {delta:+.4f}; all guardrails passed", checks, delta


def _key_metrics(res: dict, k_values: list[int]) -> dict:
    r, e = res["retrieval"], res["retrieval_with_abstention"]
    out = {"n_train_answerable": r.get("n", 0), "n_train_unanswerable": res["abstention"]["n_unanswerable"]}
    for k in k_values:
        for m in ("precision", "recall", "f1"):
            out[f"{m}@{k}"] = r.get(f"{m}@{k}")
            out[f"e2e_{m}@{k}"] = e.get(f"{m}@{k}")
    out.update({f"abstention.{k}": v for k, v in res["abstention"].items()})
    out["offset_errors"] = res["offset_errors"]
    out["threshold"] = res["config"]["abstention"]["threshold"]
    return out


def choose_candidate(remaining: list[dict], dominant: str | None) -> tuple[dict, str]:
    if dominant:
        for c in remaining:
            if dominant in c.get("tags", []):
                return c, f"rule: dominant failure '{dominant}' matches tags"
    return remaining[0], "queue: next predeclared candidate"


def run_loop(base_cfg: dict, dataset: Dataset, spec: dict, run_dir: str | Path,
             log=print, max_iterations: int | None = None) -> dict:
    protocol = spec["protocol"]
    max_it = int(max_iterations or protocol.get("max_iterations", len(spec["candidates"])))
    min_it = int(protocol.get("min_iterations", 5))
    run_dir = resolve_path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    it_log = run_dir / "iterations.jsonl"
    it_log.write_text("", encoding="utf-8")

    # Train-only view of the data: test queries are not even present.
    train = Dataset(queries=dataset.split("train", True), negatives=dataset.split("train", False),
                    documents=dataset.documents, meta=dict(dataset.meta))
    assert all(q.split == "train" for q in train.queries + train.negatives)
    neg_hash = unanswerable_set_hash(base_cfg)
    (run_dir / "loop_spec.yaml").write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
    k_values = list(base_cfg["evaluation"]["k_values"])

    def write_iter(rec: dict) -> None:
        with open(it_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")

    def run_one(cfg: dict, label: str) -> tuple[dict, dict]:
        t0 = time.time()
        res = evaluate(cfg, train, "train", calibrate_on_train=True)
        out = write_results(res, run_dir / label)
        summ = error_analysis(res["per_query"], res["config"], train.documents, out / "diagnostics", label)
        res["_elapsed_s"] = round(time.time() - t0, 2)
        res["_diag"] = summ
        log(format_summary(res))
        return res, summ

    log(f"[loop] baseline: {base_cfg.get('name')}  (train answerable={len(train.queries)}, "
        f"train unanswerable={len(train.negatives)})")
    accepted_res, diag = run_one(copy.deepcopy(base_cfg), "iter00_baseline")
    accepted_cfg = accepted_res["config"]
    dump_config(accepted_cfg, run_dir / "accepted_config.yaml")
    write_iter({"iteration": 0, "candidate_id": "baseline", "proposer": "baseline",
                "hypothesis": "Initial configuration (reference point).", "changes": {},
                "metrics": _key_metrics(accepted_res, k_values), "diagnostic_counts": diag["counts"],
                "decision": "accepted", "reason": "baseline", "accepted_after": "baseline",
                "config_fingerprint": config_fingerprint(accepted_cfg), "timestamp": _now(),
                "git": _git_rev(), "elapsed_s": accepted_res["_elapsed_s"]})
    accepted_id = "baseline"

    remaining = list(spec["candidates"])
    evaluated, skipped = 0, []
    history = []
    while remaining and evaluated < max_it:
        cand, why = choose_candidate(remaining, diag.get("dominant_answerable_failure"))
        remaining.remove(cand)
        changes = resolve_changes(accepted_cfg, cand.get("changes", {}))
        rec = {"candidate_id": cand["id"], "proposer": why, "trigger_dominant_failure":
               diag.get("dominant_answerable_failure"), "hypothesis": cand.get("hypothesis", ""),
               "changes": changes, "relative_to": accepted_id, "timestamp": _now(), "git": _git_rev()}
        if cand.get("requires") == "dense" and not dense_available():
            rec.update({"iteration": None, "decision": "skipped",
                        "reason": "optional dependency missing (uv sync --extra dense)"})
            write_iter(rec)
            skipped.append(cand["id"])
            log(f"[loop] SKIP {cand['id']}: dense extra not installed")
            continue
        cfg = apply_overrides(accepted_cfg, changes)
        cfg["name"] = cand["id"]
        cfg["status"] = "candidate"
        try:
            validate_config(cfg)
        except ValueError as e:
            rec.update({"iteration": None, "decision": "skipped", "reason": f"invalid config: {e}"})
            write_iter(rec)
            skipped.append(cand["id"])
            log(f"[loop] SKIP {cand['id']}: {e}")
            continue
        if config_fingerprint(cfg) == config_fingerprint(accepted_cfg):
            rec.update({"iteration": None, "decision": "skipped", "reason": "no-op: identical to accepted"})
            write_iter(rec)
            skipped.append(cand["id"])
            continue
        evaluated += 1
        log(f"\n[loop] iteration {evaluated}: {cand['id']} ({why})\n  hypothesis: {rec['hypothesis']}\n"
            f"  changes: {changes}")
        label = f"iter{evaluated:02d}_{cand['id']}"
        try:
            res, cdiag = run_one(cfg, label)
        except Exception as e:  # keep the loop alive; log the failure as a rejection
            rec.update({"iteration": evaluated, "decision": "rejected", "reason": f"error: {e!r}"})
            write_iter(rec)
            log(f"[loop] ERROR {cand['id']}: {e!r}")
            continue
        ok, reason, checks, delta = compare(res, accepted_res, protocol)
        rec.update({"iteration": evaluated, "metrics": _key_metrics(res, k_values),
                    "diagnostic_counts": cdiag["counts"], "primary_metric": protocol["primary_metric"],
                    "primary_delta": delta, "guardrails": checks, "decision": "accepted" if ok else "rejected",
                    "reason": reason, "config_fingerprint": config_fingerprint(res["config"]),
                    "elapsed_s": res["_elapsed_s"]})
        if ok:
            accepted_res, accepted_cfg, diag, accepted_id = res, res["config"], cdiag, cand["id"]
            dump_config(accepted_cfg, run_dir / "accepted_config.yaml")
        rec["accepted_after"] = accepted_id
        write_iter(rec)
        history.append(rec)
        log(f"[loop] {rec['decision'].upper()}: {reason}")
        if unanswerable_set_hash(base_cfg) != neg_hash:
            raise RuntimeError("Frozen unanswerable set changed during the loop - aborting.")

    summary = {"run_dir": str(run_dir), "iterations_evaluated": evaluated, "skipped": skipped,
               "min_iterations_required": min_it, "met_min_iterations": evaluated >= min_it,
               "accepted_candidate": accepted_id, "accepted_metrics": _key_metrics(accepted_res, k_values),
               "protocol": protocol, "unanswerable_sha256": neg_hash, "finished": _now()}
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log(f"\n[loop] done. evaluated={evaluated} accepted={accepted_id} -> {run_dir / 'accepted_config.yaml'}")
    if evaluated < min_it:
        log(f"[loop] WARNING: only {evaluated} iterations evaluated (< {min_it}).")
    return summary

