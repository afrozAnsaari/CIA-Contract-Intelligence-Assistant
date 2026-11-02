"""Offset-preserving chunking.

Invariant: for every chunk, ``source_text[start:end] == chunk.text``. The source text is
never modified; chunk boundaries are only *positions* in the original string.

Strategy "paragraph": windows of at most ``max_chars`` whose end is moved back to the best
natural boundary within the last ``boundary_search_frac`` of the window, preferring
paragraph break > sentence end > whitespace > hard cut. Oversized paragraphs therefore
get split at sentence/word boundaries without losing positions.
Strategy "fixed": hard cuts every ``max_chars`` (minus overlap).
Overlap: the next window starts at (end - overlap_chars), moved forward to a word start.
"""

from __future__ import annotations

import bisect
import re
from dataclasses import dataclass

PARA_RE = re.compile(r"\n[ \t\r\f\v]*\n")
SENT_RE = re.compile(r"[.;:!?][\"')\]]*(?=\s)")
WS_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class Chunk:
    chunk_id: int
    document_id: str
    start: int
    end: int
    text: str


def _boundaries(text: str) -> tuple[list[int], list[int], list[int]]:
    para = [m.end() for m in PARA_RE.finditer(text)]
    sent = [m.end() for m in SENT_RE.finditer(text)]
    ws = [m.start() for m in WS_RE.finditer(text)]  # cut *before* whitespace
    return para, sent, ws


def _last_in(sorted_list: list[int], lo: int, hi: int) -> int | None:
    """Largest value v in sorted_list with lo < v <= hi."""
    i = bisect.bisect_right(sorted_list, hi) - 1
    if i >= 0 and sorted_list[i] > lo:
        return sorted_list[i]
    return None


def _skip_ws(text: str, pos: int) -> int:
    n = len(text)
    while pos < n and text[pos].isspace():
        pos += 1
    return pos


def _rstrip_pos(text: str, start: int, end: int) -> int:
    while end > start and text[end - 1].isspace():
        end -= 1
    return end


def chunk_spans(text: str, max_chars: int, overlap_chars: int, strategy: str = "paragraph",
                boundary_search_frac: float = 0.3, min_chars: int = 1) -> list[tuple[int, int]]:
    n = len(text)
    if max_chars <= 0 or not 0 <= overlap_chars < max_chars:
        raise ValueError("require max_chars > 0 and 0 <= overlap_chars < max_chars")
    para, sent, ws = _boundaries(text) if strategy == "paragraph" else ([], [], [])
    spans: list[tuple[int, int]] = []
    start = _skip_ws(text, 0)
    while start < n:
        hard_end = min(start + max_chars, n)
        end = hard_end
        if hard_end < n and strategy == "paragraph":
            lo = start + int(max_chars * (1.0 - boundary_search_frac))
            for cands in (para, sent, ws):
                b = _last_in(cands, lo, hard_end)
                if b is not None:
                    end = b
                    break
        end = _rstrip_pos(text, start, end)
        if end <= start:  # whitespace-only window (cannot happen after _skip_ws, defensive)
            end = hard_end
        spans.append((start, end))
        if end >= _rstrip_pos(text, 0, n):
            break
        if overlap_chars > 0:
            nxt = max(end - overlap_chars, start + 1)
            if strategy == "paragraph":
                # move forward to the next word start so chunks don't begin mid-word
                while nxt < end and not (text[nxt - 1].isspace() and not text[nxt].isspace()):
                    nxt += 1
                if nxt >= end:
                    nxt = end
        else:
            nxt = end
        start = _skip_ws(text, nxt)
    if min_chars > 1 and len(spans) > 1:
        spans = [s for s in spans if s[1] - s[0] >= min_chars] or spans
    return spans


def chunk_document(document_id: str, text: str, chunk_cfg: dict, start_id: int = 0) -> list[Chunk]:
    spans = chunk_spans(text, int(chunk_cfg["max_chars"]), int(chunk_cfg["overlap_chars"]),
                        chunk_cfg.get("strategy", "paragraph"), float(chunk_cfg.get("boundary_search_frac", 0.3)),
                        int(chunk_cfg.get("min_chars", 1)))
    return [Chunk(start_id + i, document_id, s, e, text[s:e]) for i, (s, e) in enumerate(spans)]


def chunk_corpus(documents: dict[str, str], chunk_cfg: dict) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc_id in sorted(documents):
        chunks.extend(chunk_document(doc_id, documents[doc_id], chunk_cfg, start_id=len(chunks)))
    return chunks


def validate_chunks(chunks: list[Chunk], documents: dict[str, str]) -> int:
    """Return the number of chunks violating the offset invariant (should be 0)."""
    return sum(1 for c in chunks if documents[c.document_id][c.start:c.end] != c.text)
