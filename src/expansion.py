"""Controlled legal query expansion for the RANKING query only (never for abstention signals).

Each rule fires when its trigger pattern matches the (lowercased) question text and adds a
small, fixed list of clause vocabulary that contracts commonly use for that concept, e.g.
"audit rights" -> books, records, inspect. Expansion terms get a reduced weight
(`query.expansion_weight`), so they can lift a relevant clause without overriding the
words the user actually typed. Rules are generic contract-drafting vocabulary written from
domain knowledge, keyed by concept; none references a specific contract or gold span.
"""

from __future__ import annotations

import re

RULES: list[tuple[str, list[str]]] = [
    (r"governing law|governed by|choice of law", ["governed", "construed", "laws", "jurisdiction"]),
    (r"expir|expiration", ["term", "expire", "remain in effect", "continue in full force", "years"]),
    (r"renew", ["renew", "renewal", "automatically", "successive", "extend"]),
    (r"assign", ["assign", "transfer", "consent", "prior written consent"]),
    (r"change of control", ["change of control", "merger", "acquisition", "acquire", "control"]),
    (r"audit", ["audit", "inspect", "inspection", "examine", "books", "records", "access"]),
    (r"liabilit", ["liable", "liability", "exceed", "aggregate", "damages", "limitation"]),
    (r"insurance", ["insurance", "insured", "policy", "coverage"]),
    (r"convenience", ["terminate", "without cause", "at any time", "notice", "discretion"]),
    (r"exclusiv", ["exclusive", "exclusively", "sole"]),
    (r"compet", ["compete", "competing", "competitive", "engage"]),
    (r"exception", ["except", "notwithstanding", "provided that", "nothing", "prevent"]),
    (r"licen[cs]", ["license", "grant", "right to use"]),
    (r"transferable|transfer", ["transfer", "transferable", "assign", "sublicense"]),
    (r"intellectual property", ["intellectual property", "own", "ownership", "title", "vest", "inventions"]),
    (r"joint", ["joint", "jointly"]),
    (r"irrevocable|perpetual", ["irrevocable", "perpetual"]),
    (r"first refusal|first offer|first negotiation", ["first refusal", "first offer", "negotiate"]),
    (r"revenue|profit", ["royalty", "royalties", "percent", "share", "revenue", "profit", "commission"]),
    (r"minimum commitment", ["minimum", "at least", "purchase", "commit"]),
    (r"volume", ["volume", "quantity", "maximum", "units"]),
    (r"third.party beneficiar", ["third party beneficiary", "beneficiaries"]),
    (r"solicit", ["solicit", "hire", "employ", "induce"]),
    (r"covenant not to sue", ["sue", "challenge", "contest", "claim"]),
    (r"warrant", ["warrant", "warranty", "warranties", "period", "days", "months"]),
    (r"disparag", ["disparage", "disparaging", "negative statements"]),
    (r"most favou?red", ["most favored", "favorable", "no less favorable"]),
    (r"after (the )?termination|post.termination", ["after termination", "following termination", "transition", "survive"]),
    (r"notice period", ["notice", "prior written notice", "days"]),
]
# Function words that can appear inside an expansion phrase ("at any time") but carry no clause
# meaning; with query.expansion_skip_function_words they are not added as expansion terms.
EXPANSION_FUNCTION_WORDS = frozenset({"any", "all", "each", "every", "less", "such", "other"})

_COMPILED = [(re.compile(p), terms) for p, terms in RULES]


def expansion_phrases(question: str) -> list[str]:
    """Deterministic, ordered list of expansion phrases triggered by the question text."""
    q = question.lower()
    out: list[str] = []
    for pat, terms in _COMPILED:
        if pat.search(q):
            out.extend(t for t in terms if t not in out)
    return out
