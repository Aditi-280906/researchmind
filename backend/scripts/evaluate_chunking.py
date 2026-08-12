import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ingestion.pipeline import process_pdf
from app.ingestion.chunking.paragraph import ParagraphChunker


def evaluate(pdf_paths, target_tokens, overlap_tokens):
    all_chunks = []
    for pdf_path in pdf_paths:
        chunker = ParagraphChunker(target_tokens=target_tokens, overlap_tokens=overlap_tokens)
        chunks = process_pdf(pdf_path, chunker=chunker)
        all_chunks.extend(chunks)

    if not all_chunks:
        print("No chunks produced.")
        return

    token_counts = [c.token_count for c in all_chunks]
    print(f"=== {target_tokens} TOKEN CHUNKING (overlap={overlap_tokens}) ===")
    print(f"Documents: {len(pdf_paths)}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Average chunk size: {sum(token_counts) / len(token_counts):.0f}")
    print(f"Minimum: {min(token_counts)}")
    print(f"Maximum: {max(token_counts)}")
    print()


def main():
    papers_dir = Path("data/papers")
    pdf_paths = [str(p) for p in papers_dir.glob("*.pdf")]

    for target in [200, 400, 600, 800]:
        evaluate(pdf_paths, target_tokens=target, overlap_tokens=int(target * 0.1))


if __name__ == "__main__":
    main()