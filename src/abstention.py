"""Abstention: a method-specific threshold over one documented relevance signal.

Rule (exact):  abstain  iff  there are no candidate passages  OR  signal < threshold.
At equality (signal == threshold) the system ANSWERS.

Signals (none of them is a probability):
  chunk_bm25_norm : best BM25 chunk score / query-dependent BM25 upper bound, in [0, 1)
  chunk_full_bm25_norm : same as chunk_bm25_norm but always computed with the FULL query
                    (contract preamble + question) over the routed chunks, even when ranking
                    uses only the question part; decouples abstention from ranking.
  chunk_split_bm25_norm : (best chunk score of the contract preamble + best chunk score of the
                    question) / (upper bound of preamble + upper bound of question), over the
                    routed contract's chunks. Unlike chunk_full_bm25_norm it does not require one
                    chunk to match both parts (the preamble matches the header, the question the
                    clause). Equals chunk_full_bm25_norm when the query has no preamble.
  preamble_bm25_norm : best chunk score of the contract preamble / its upper bound (identity).
  identity_and_question : two-part rule (needs split mode + routing): abstain iff
                    preamble_bm25_norm < doc_threshold (contract identity not confirmed) OR
                    chunk_bm25_norm < threshold (question-only answerability). Jointly calibrated.
  doc_bm25_norm   : same normalisation at document-routing level
  dense_max_cos   : best cosine similarity (dense / hybrid only), in [-1, 1]
  doc_and_chunk   : two-part rule (needs doc routing): abstain iff
                    doc_bm25_norm < doc_threshold  OR  chunk_bm25_norm < threshold.
                    The doc part asks "does the named contract exist?", the chunk part
                    asks "does the question match any passage of the routed contract?".
                    Equality on either part => that part passes.
Raw BM25, cosine and RRF scores are not comparable, so each config is calibrated
separately, on TRAIN answerable queries + TRAIN unanswerable queries only.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Decision:
    abstained: bool
    reason: str  # answered | no_candidates | below_threshold | disabled_no_candidates
    signal: str
    value: float | None
    threshold: float
    doc_value: float | None = None
    doc_threshold: float | None = None


def decide(n_candidates: int, signals: dict[str, float], abst_cfg: dict) -> Decision:
    name, thr = abst_cfg["signal"], float(abst_cfg["threshold"])
    if name in DUAL_SIGNALS:
        return _decide_dual(n_candidates, signals, abst_cfg)
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


# two-part rules: name -> (identity/document signal, answerability signal)
DUAL_SIGNALS = {"doc_and_chunk": ("doc_bm25_norm", "chunk_bm25_norm"),
                "identity_and_question": ("preamble_bm25_norm", "chunk_bm25_norm")}


def _decide_dual(n_candidates: int, signals: dict[str, float], abst_cfg: dict) -> Decision:
    name = abst_cfg["signal"]
    id_key, ans_key = DUAL_SIGNALS[name]
    thr, dthr = float(abst_cfg["threshold"]), float(abst_cfg.get("doc_threshold", 0.0))
    cv, dv = signals.get(ans_key), signals.get(id_key)
    mk = lambda ab, why: Decision(ab, why, name, cv, thr, dv, dthr)  # noqa: E731
    if n_candidates == 0:
        return mk(True, "no_candidates")
    if not abst_cfg.get("enabled", True):
        return mk(False, "answered")
    if cv is None or dv is None:
        raise KeyError(f"{name} needs {id_key} and {ans_key} (enable doc routing / split mode)")
    if dv < dthr:
        return mk(True, "below_doc_threshold")
    if cv < thr:
        return mk(True, "below_threshold")
    return mk(False, "answered")


def _candidates(vals: list[float]) -> list[float]:
    v = sorted(set(vals))
    return [v[0]] + [(a + b) / 2 for a, b in zip(v, v[1:])] + [v[-1] + 1e-9]


def calibrate_dual(pos: list[tuple[float, float]], neg: list[tuple[float, float]]) -> dict:
    """Joint grid search over (doc_threshold, chunk_threshold); pairs are (doc, chunk).

    Candidates per axis as in `calibrate`. Maximise balanced accuracy; ties broken by
    higher answer rate on answerable, then smaller doc_threshold, then smaller chunk threshold.
    """
    if not pos and not neg:
        return {"threshold": 0.0, "doc_threshold": 0.0, "balanced_accuracy": None, "n_pos": 0, "n_neg": 0}
    allp = pos + neg
    td = np.array(_candidates([d for d, _ in allp]))
    tc = np.array(_candidates([c for _, c in allp]))

    def answered(pairs):  # fraction answered for every (td, tc) combination, shape (A, B)
        if not pairs:
            return np.zeros((len(td), len(tc)))
        arr = np.array(pairs, dtype=np.float64)
        dm = (arr[None, :, 0] >= td[:, None]).astype(np.float64)  # (A, P)
        cm = (arr[None, :, 1] >= tc[:, None]).astype(np.float64)  # (B, P)
        return dm @ cm.T / len(pairs)

    ans_pos, ans_neg = answered(pos), answered(neg)
    if pos and neg:
        ba = 0.5 * (ans_pos + (1.0 - ans_neg))
    else:
        ba = ans_pos if pos else 1.0 - ans_neg
    best = None
    for a in range(len(td)):
        for b in range(len(tc)):
            key = (round(float(ba[a, b]), 12), round(float(ans_pos[a, b]), 12), -td[a], -tc[b])
            if best is None or key > best[0]:
                best = (key, a, b)
    _, a, b = best
    return {"threshold": float(tc[b]), "doc_threshold": float(td[a]), "balanced_accuracy": float(ba[a, b]),
            "answer_rate_answerable": float(ans_pos[a, b]), "abstain_rate_unanswerable": float(1 - ans_neg[a, b]),
            "n_pos": len(pos), "n_neg": len(neg)}


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
