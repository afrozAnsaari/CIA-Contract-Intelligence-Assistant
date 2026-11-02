"""Character-level precision / recall (LegalBench-RAG, Pipitone & Houir Alami 2024).

For one query with gold character set G and the character set R covered by the top-k
retrieved passages (characters identified by (document_id, offset)):
    Precision@k = |R ∩ G| / |R|      (0 if nothing retrieved)
    Recall@k    = |R ∩ G| / |G|
Aggregate = unweighted mean over queries (macro), reported with its query count.
Character sets are unions, so duplicate/overlapping passages are not double counted; the
authors' reference code sums pairwise overlaps without merging, which is identical when
returned passages do not overlap (our default overlap_policy "skip"/"trim" guarantees
this). The pairwise variant is also computed (`ref_*`) for transparency.
F1@k (our selection objective, not a benchmark metric) = per-query harmonic mean of P@k
and R@k (0 if both are 0), averaged over queries.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

Span = tuple[str, int, int]  # (document_id, start, end)


def merge_intervals(iv: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    out: list[list[int]] = []
    for s, e in sorted(iv):
        if e <= s:
            continue
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def _by_doc(spans: Iterable[Span]) -> dict[str, list[tuple[int, int]]]:
    d: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for doc, s, e in spans:
        d[doc].append((s, e))
    return {k: merge_intervals(v) for k, v in d.items()}


def _intersection(a: list[tuple[int, int]], b: list[tuple[int, int]]) -> int:
    i = j = tot = 0
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if hi > lo:
            tot += hi - lo
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return tot


def precision_recall(retrieved: list[Span], gold: list[Span]) -> tuple[float, float]:
    R, G = _by_doc(retrieved), _by_doc(gold)
    r_len = sum(e - s for v in R.values() for s, e in v)
    g_len = sum(e - s for v in G.values() for s, e in v)
    inter = sum(_intersection(R[d], G[d]) for d in R if d in G)
    p = inter / r_len if r_len else 0.0
    r = inter / g_len if g_len else 0.0
    return p, r


def reference_precision_recall(retrieved: list[Span], gold: list[Span]) -> tuple[float, float]:
    """Pairwise-sum variant mirroring the authors' reference implementation."""
    def ov(a: Span, b: Span) -> int:
        return max(0, min(a[2], b[2]) - max(a[1], b[1])) if a[0] == b[0] else 0
    r_len = sum(e - s for _, s, e in retrieved)
    g_len = sum(e - s for _, s, e in gold)
    inter = sum(ov(r, g) for r in retrieved for g in gold)
    return (inter / r_len if r_len else 0.0), (inter / g_len if g_len else 0.0)


def f1(p: float, r: float) -> float:
    return 2 * p * r / (p + r) if p + r > 0 else 0.0


def metrics_at_k(retrieved: list[Span], gold: list[Span], k_values: list[int]) -> dict[str, float]:
    out: dict[str, float] = {}
    for k in k_values:
        top = retrieved[:k]
        p, r = precision_recall(top, gold)
        rp, rr = reference_precision_recall(top, gold)
        out[f"precision@{k}"] = p
        out[f"recall@{k}"] = r
        out[f"f1@{k}"] = f1(p, r)
        out[f"ref_precision@{k}"] = rp
        out[f"ref_recall@{k}"] = rr
    return out


def mean_metrics(rows: list[dict[str, float]]) -> dict[str, float]:
    if not rows:
        return {"n": 0}
    keys = rows[0].keys()
    out = {k: sum(r[k] for r in rows) / len(rows) for k in keys}
    out["n"] = len(rows)
    return out


def abstention_metrics(answerable_abstained: list[bool], unanswerable_abstained: list[bool]) -> dict:
    """Denominators: answerable queries for false abstention; unanswerable for the rest."""
    na, nu = len(answerable_abstained), len(unanswerable_abstained)
    fa = sum(answerable_abstained)
    ca = sum(unanswerable_abstained)
    far = fa / na if na else None
    car = ca / nu if nu else None
    out = {
        "n_answerable": na,
        "n_unanswerable": nu,
        "false_abstentions": fa,
        "false_abstention_rate": far,  # abstained on answerable / #answerable
        "correct_abstentions": ca,
        "correct_abstention_rate": car,  # abstained on unanswerable / #unanswerable
        "failures_to_abstain": nu - ca,
        "failure_to_abstain_rate": (nu - ca) / nu if nu else None,
    }
    out["balanced_accuracy"] = (0.5 * ((1 - far) + car)) if na and nu else None
    return out
