"""Abstention: a method-specific threshold over one documented relevance signal.

Rule (exact):  abstain  iff  there are no candidate passages  OR  signal < threshold.
At equality (signal == threshold) the system ANSWERS.

Signals (none of them is a probability):
  chunk_bm25_norm : best BM25 chunk score / query-dependent BM25 upper bound, in [0, 1)
  doc_bm25_norm   : same normalisation at document-routing level
  dense_max_cos   : best cosine similarity (dense / hybrid only), in [-1, 1]
Raw BM25, cosine and RRF scores are not comparable, so each config is calibrated
separately, on TRAIN answerable queries + TRAIN unanswerable queries only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Decision:
    abstained: bool
    reason: str  # answered | no_candidates | below_threshold | disabled_no_candidates
    signal: str
    value: float | None
    threshold: float


def decide(n_candidates: int, signals: dict[str, float], abst_cfg: dict) -> Decision:
    name, thr = abst_cfg["signal"], float(abst_cfg["threshold"])
    value = signals.get(name)
    if n_candidates == 0:
        return Decision(True, "no_candidates", name, value, thr)
    if not abst_cfg.get("enabled", True):
        return Decision(False, "answered", name, value, thr)
    if value is None:
        raise KeyError(f"Abstention signal {name!r} not produced by this retrieval config")
    if value < thr:
        return Decision(True, "below_threshold", name, value, thr)
    return Decision(False, "answered", name, value, thr)


def calibrate(pos: list[float], neg: list[float]) -> dict:
    """Choose the threshold maximising balanced accuracy on (answerable=pos, unanswerable=neg).

    Candidate thresholds: the minimum observed value (answer everything), midpoints
    between consecutive distinct observed values, and max + 1e-9 (abstain on all).
    Balanced accuracy = 0.5 * (answer rate on pos + abstention rate on neg).
    Ties are broken by the SMALLEST threshold (prefer fewer false abstentions).
    """
    vals = sorted(set(pos) | set(neg))
    if not vals:
        return {"threshold": 0.0, "balanced_accuracy": None, "n_pos": 0, "n_neg": 0}
    cands = [vals[0]] + [(a + b) / 2 for a, b in zip(vals, vals[1:])] + [vals[-1] + 1e-9]
    best = None
    for t in cands:
        ans_pos = sum(v >= t for v in pos) / len(pos) if pos else 0.0
        abs_neg = sum(v < t for v in neg) / len(neg) if neg else 0.0
        ba = 0.5 * (ans_pos + abs_neg) if pos and neg else (ans_pos if pos else abs_neg)
        if best is None or ba > best[0] + 1e-12:
            best = (ba, t, ans_pos, abs_neg)
    ba, t, ans_pos, abs_neg = best
    return {"threshold": float(t), "balanced_accuracy": ba, "answer_rate_answerable": ans_pos,
            "abstain_rate_unanswerable": abs_neg, "n_pos": len(pos), "n_neg": len(neg)}
