import pytest

from src.chunking import chunk_corpus, chunk_spans, validate_chunks

TEXT = ("First paragraph sentence one. Sentence two is here.\n\n"
        + "A very long paragraph " * 40 + "ends here.\n\n  Third   paragraph\twith odd   spacing.  \n")


@pytest.mark.parametrize("strategy", ["paragraph", "fixed"])
@pytest.mark.parametrize("size,ov", [(50, 0), (120, 20), (300, 100), (10_000, 0)])
def test_offsets_exact_and_bounded(strategy, size, ov):
    spans = chunk_spans(TEXT, size, ov, strategy)
    assert spans
    for s, e in spans:
        assert 0 <= s < e <= len(TEXT)
        assert e - s <= size
    covered = set()
    for s, e in spans:
        covered.update(range(s, e))
    assert all(i in covered for i, ch in enumerate(TEXT) if not ch.isspace())  # no text lost


def test_chunk_invariant_on_corpus():
    docs = {"d1": TEXT, "d2": "short doc", "d3": "été \r\n café"}
    chunks = chunk_corpus(docs, {"max_chars": 80, "overlap_chars": 10, "strategy": "paragraph"})
    assert validate_chunks(chunks, docs) == 0
    assert [c.chunk_id for c in chunks] == list(range(len(chunks)))


def test_overlap_changes_behavior():
    a = chunk_spans(TEXT, 100, 0)
    b = chunk_spans(TEXT, 100, 40)
    assert len(b) > len(a)
    assert any(b[i + 1][0] < b[i][1] for i in range(len(b) - 1))
    assert all(a[i + 1][0] >= a[i][1] for i in range(len(a) - 1))


def test_paragraph_prefers_boundaries():
    spans = chunk_spans(TEXT, 70, 0, "paragraph")
    assert TEXT[spans[0][0]:spans[0][1]].endswith("Sentence two is here.")


def test_invalid_params():
    with pytest.raises(ValueError):
        chunk_spans(TEXT, 100, 100)
    assert chunk_spans("", 100, 0) == []
    assert chunk_spans("   \n ", 100, 0) == []
