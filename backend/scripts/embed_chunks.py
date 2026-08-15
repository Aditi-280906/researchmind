import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ai.embeddings.sentence_transformer import SentenceTransformerEmbedding


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/embed_chunks.py <path_to_chunks.json>")
        sys.exit(1)

    chunks_path = Path(sys.argv[1])

    with open(chunks_path) as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]

    model = SentenceTransformerEmbedding()
    embeddings = model.embed_documents(texts)

    records = []
    for chunk, embedding in zip(chunks, embeddings):
        records.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "embedding": embedding,
            "metadata": {
                "page": chunk.get("page_number"),
                "section": chunk.get("section"),
            },
        })

    output_dir = Path("data/embeddings")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / chunks_path.name

    output_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    print(f"Embedded {len(records)} chunks")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()