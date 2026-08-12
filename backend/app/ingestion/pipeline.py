from pathlib import Path

from app.ingestion.pdf_reader import read_pdf
from app.ingestion.text_cleaner import clean_text
from app.ingestion.chunking.paragraph import ParagraphChunker
from app.models.chunk import Chunk


def process_pdf(pdf_path: str, chunker=None) -> list[Chunk]:
    """
    Full pipeline: PDF -> raw text -> cleaned text -> chunks.
    """
    if chunker is None:
        chunker = ParagraphChunker()

    document_id = Path(pdf_path).stem

    raw_text = read_pdf(pdf_path)
    cleaned = clean_text(raw_text)
    chunks = chunker.chunk(cleaned, document_id=document_id)

    return chunks