import tiktoken
from app.models.chunk import Chunk
from app.ingestion.chunking.base import BaseChunker

_encoder = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    return len(_encoder.encode(text))


class ParagraphChunker(BaseChunker):
    def __init__(self, target_tokens: int = 400, overlap_tokens: int = 50):
        self.target_tokens = target_tokens
        self.overlap_tokens = overlap_tokens

    def chunk(self, text: str, document_id: str) -> list[Chunk]:
        if not text.strip():
            return []

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        chunks: list[Chunk] = []
        current_paragraphs: list[str] = []
        current_tokens = 0
        chunk_index = 0

        for paragraph in paragraphs:
            paragraph_tokens = count_tokens(paragraph)

            # If adding this paragraph would overflow the target, close the current chunk first
            if current_paragraphs and current_tokens + paragraph_tokens > self.target_tokens:
                chunk_text = "\n\n".join(current_paragraphs)
                chunks.append(self._make_chunk(chunk_text, document_id, chunk_index))
                chunk_index += 1

                # Start next chunk with overlap: carry the tail of the previous chunk forward
                overlap_text = self._get_overlap(chunk_text)
                current_paragraphs = [overlap_text] if overlap_text else []
                current_tokens = count_tokens(overlap_text) if overlap_text else 0

            current_paragraphs.append(paragraph)
            current_tokens += paragraph_tokens

        # Don't forget the final chunk
        if current_paragraphs:
            chunk_text = "\n\n".join(current_paragraphs)
            chunks.append(self._make_chunk(chunk_text, document_id, chunk_index))

        return chunks

    def _make_chunk(self, text: str, document_id: str, index: int) -> Chunk:
        return Chunk(
            chunk_id=f"{document_id}_{index:04d}",
            document_id=document_id,
            chunk_index=index,
            text=text,
            token_count=count_tokens(text),
        )

    def _get_overlap(self, text: str) -> str:
        tokens = _encoder.encode(text)
        if len(tokens) <= self.overlap_tokens:
            return text
        overlap_tokens = tokens[-self.overlap_tokens:]
        return _encoder.decode(overlap_tokens)