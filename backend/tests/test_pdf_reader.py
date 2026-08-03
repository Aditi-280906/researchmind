import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ingestion.pdf_reader import read_pdf


def test_pdf_opens_and_extracts_text():
    pdf_path = "data/papers/attention-is-all-you-need.pdf"

    text = read_pdf(pdf_path)

    assert text is not None
    assert len(text) > 0


if __name__ == "__main__":
    test_pdf_opens_and_extracts_text()
    print("Test passed: PDF opened and text extracted successfully.")