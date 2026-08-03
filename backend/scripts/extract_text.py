import sys
from pathlib import Path

# Allow importing from app/ when running this script directly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ingestion.pdf_reader import read_pdf


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/extract_text.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    text = read_pdf(pdf_path)

    print(f"Text length: {len(text)} characters")
    print("\nFirst 500 characters:\n")
    print(text[:500])


if __name__ == "__main__":
    main()