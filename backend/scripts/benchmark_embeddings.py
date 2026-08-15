import sys
import json
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ai.embeddings.sentence_transformer import SentenceTransformerEmbedding


def load_all_chunks() -> list[str]:
    """Pool chunks from every paper we've processed, so we have enough to test at scale."""
    texts = []
    chunks_dir = Path("data/chunks")
    for file in chunks_dir.glob("*.json"):
        with open(file) as f:
            chunks = json.load(f)
        texts.extend(c["text"] for c in chunks)
    return texts


def benchmark(model: SentenceTransformerEmbedding, texts: list[str], n: int):
    # Repeat the pool if we don't have enough real chunks to hit n
    sample = (texts * ((n // len(texts)) + 1))[:n]

    start = time.time()
    model.embed_documents(sample)
    elapsed = time.time() - start

    chunks_per_second = n / elapsed if elapsed > 0 else float("inf")

    print(f"{n:<8}{elapsed:.2f}s{'':<8}{chunks_per_second:.1f} chunks/sec")


def main():
    texts = load_all_chunks()
    print(f"Loaded {len(texts)} real chunks from data/chunks/ (will repeat if needed)\n")

    model = SentenceTransformerEmbedding()

    print(f"{'Chunks':<8}{'Time':<10}{'Speed'}")
    for n in [10, 100, 500, 1000]:
        benchmark(model, texts, n)


if __name__ == "__main__":
    main()