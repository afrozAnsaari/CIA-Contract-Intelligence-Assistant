"""Search-only text normalisation (tokenisation). Never applied to returned source text."""

from __future__ import annotations

import re
from functools import lru_cache

import snowballstemmer

TOKEN_RE = re.compile(r"[A-Za-z0-9]+")

# Small, fixed English stopword list (kept in code so it is versioned and inspectable).
STOPWORDS = frozenset(
    """a an and are as at be been but by can could did do does for from had has have he her his i if in
    into is it its may me more most must my no nor not of on or our out over shall she should so such than
    that the their them then there these they this those to under up upon us was we were what when where
    which while who whom why will with would you your""".split()
)

_STEMMER = snowballstemmer.stemmer("english")


@lru_cache(maxsize=200_000)
def _stem(tok: str) -> str:
    return _STEMMER.stemWord(tok)


def tokenize(text: str, lowercase: bool = True, stopwords: bool = False, stemming: bool = False) -> list[str]:
    toks = TOKEN_RE.findall(text)
    if lowercase:
        toks = [t.lower() for t in toks]
    if stopwords:
        toks = [t for t in toks if t.lower() not in STOPWORDS]
    if stemming:
        toks = [_stem(t) for t in toks]
    return toks


def make_tokenizer(text_cfg: dict):
    lc, sw, st = bool(text_cfg["lowercase"]), bool(text_cfg["stopwords"]), bool(text_cfg["stemming"])
    return lambda s: tokenize(s, lc, sw, st)


PREAMBLE_RE = re.compile(r"^\s*Consider\s+(?P<pre>.*?);\s*(?P<q>.+)$", re.IGNORECASE | re.DOTALL)


def split_query(query: str) -> tuple[str, str]:
    """Split a CUAD-style query into (contract preamble, question).

    Uses only the query string. If there is no "Consider ...;" preamble, the preamble
    is empty and the question is the whole query.
    """
    m = PREAMBLE_RE.match(query)
    if not m:
        return "", query.strip()
    return m.group("pre").strip(), m.group("q").strip()


def title_from_document_id(document_id: str) -> str:
    """Human-readable title derived from the CUAD file name (a public source identifier)."""
    name = document_id.rsplit("/", 1)[-1]
    if name.endswith(".txt"):
        name = name[:-4]
    return re.sub(r"[_\-]+", " ", name)
