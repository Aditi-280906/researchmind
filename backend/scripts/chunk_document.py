import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ingestion.pipeline import process_pdf


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/chunk_document.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    chunks = process_pdf(pdf_path)

    document_id = Path(pdf_path).stem
    output_dir = Path("data/chunks")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{document_id}.json"

    output_path.write_text(
        json.dumps([c.model_dump() for c in chunks], indent=2),
        encoding="utf-8",
    )

    print(f"Created {len(chunks)} chunks")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()