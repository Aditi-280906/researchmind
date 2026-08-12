import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.ingestion.chunking.paragraph import ParagraphChunker


def test_empty_input_returns_empty_list():
    chunker = ParagraphChunker()
    result = chunker.chunk("", document_id="doc1")
    assert result == []


def test_short_document_returns_one_chunk():
    chunker = ParagraphChunker(target_tokens=400)
    text = "This is a short paragraph about testing."
    result = chunker.chunk(text, document_id="doc1")
    assert len(result) == 1


def test_large_document_returns_multiple_chunks():
    chunker = ParagraphChunker(target_tokens=50, overlap_tokens=5)
    paragraphs = [f"This is paragraph number {i} with some extra words to pad it out." for i in range(20)]
    text = "\n\n".join(paragraphs)
    result = chunker.chunk(text, document_id="doc1")
    assert len(result) > 1


def test_chunks_have_required_metadata():
    chunker = ParagraphChunker()
    text = "Some paragraph text here."
    result = chunker.chunk(text, document_id="doc1")
    for c in result:
        assert c.chunk_id
        assert c.document_id == "doc1"
        assert c.chunk_index is not None


def test_no_major_data_loss():
    chunker = ParagraphChunker(target_tokens=50, overlap_tokens=5)
    paragraphs = [f"Paragraph {i} unique content marker{i}." for i in range(10)]
    text = "\n\n".join(paragraphs)
    result = chunker.chunk(text, document_id="doc1")
    combined = " ".join(c.text for c in result)
    for i in range(10):
        assert f"marker{i}" in combined


if __name__ == "__main__":
    test_empty_input_returns_empty_list()
    test_short_document_returns_one_chunk()
    test_large_document_returns_multiple_chunks()
    test_chunks_have_required_metadata()
    test_no_major_data_loss()
    print("All tests passed.")