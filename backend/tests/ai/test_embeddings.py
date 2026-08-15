import sys
import math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.ai.embeddings.sentence_transformer import SentenceTransformerEmbedding

# Load once, reuse across tests (loading the model is slow)
model = SentenceTransformerEmbedding()


def test_same_text_same_embedding():
    text = "The Transformer architecture relies on attention."
    emb1 = model.embed_text(text)
    emb2 = model.embed_text(text)
    assert emb1 == emb2


def test_embedding_has_expected_dimension():
    embedding = model.embed_text("Hello world")
    assert len(embedding) == 384  # BGE-small's known output size


def test_batch_embedding_returns_expected_count():
    texts = [f"Sentence number {i}" for i in range(10)]
    embeddings = model.embed_documents(texts)
    assert len(embeddings) == 10


def test_empty_input_is_handled():
    embeddings = model.embed_documents([])
    assert embeddings == []


def test_no_nan_or_infinite_values():
    embedding = model.embed_text("A normal sentence.")
    for value in embedding:
        assert not math.isnan(value)
        assert not math.isinf(value)


if __name__ == "__main__":
    test_same_text_same_embedding()
    test_embedding_has_expected_dimension()
    test_batch_embedding_returns_expected_count()
    test_empty_input_is_handled()
    test_no_nan_or_infinite_values()
    print("All tests passed.")