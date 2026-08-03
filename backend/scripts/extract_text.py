import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ingestion.pdf_reader import read_pdf
from app.ingestion.text_cleaner import clean_text


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/extract_text.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])

    raw_text = read_pdf(str(pdf_path))
    text = clean_text(raw_text)

    print(f"Text length: {len(text)} characters")
    print("\nFirst 500 characters:\n")
    print(text[:500])

    output_dir = Path("data/extracted")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / (pdf_path.stem + ".txt")
    output_path.write_text(text, encoding="utf-8")

    print(f"\nSaved cleaned text to: {output_path}")


if __name__ == "__main__":
    main()