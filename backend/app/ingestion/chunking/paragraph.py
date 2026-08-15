import tiktoken
from app.models.chunk import Chunk
from app.ingestion.chunking.base import BaseChunker
from app.ingestion.chunking.fallback import split_oversized_text, count_tokens

_encoder = tiktoken.get_encoding("cl100k_base")


class ParagraphChunker(BaseChunker):
    def __init__(self, target_tokens: int = 400, overlap_tokens: int = 50):
        self.target_tokens = target_tokens
        self.overlap_tokens = overlap_tokens

    def chunk(self, text: str, document_id: str) -> list[Chunk]:
        if not text.strip():
            return []

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        safe_units: list[str] = []
        for paragraph in paragraphs:
            if count_tokens(paragraph) > self.target_tokens:
                safe_units.extend(
                    split_oversized_text(paragraph, self.target_tokens, self.overlap_tokens)
                )
            else:
                safe_units.append(paragraph)

        chunks: list[Chunk] = []
        current_units: list[str] = []
        current_tokens = 0
        chunk_index = 0

        for unit in safe_units:
            unit_tokens = count_tokens(unit)

            if current_units and current_tokens + unit_tokens > self.target_tokens:
                chunk_text = "\n\n".join(current_units)
                chunks.append(self._make_chunk(chunk_text, document_id, chunk_index))
                chunk_index += 1

                overlap_text = self._get_overlap(chunk_text)
                overlap_tokens_count = count_tokens(overlap_text) if overlap_text else 0

                # Only carry the overlap forward if it still leaves room for this unit.
                # Otherwise, start the next chunk fresh with just this unit.
                if overlap_text and overlap_tokens_count + unit_tokens <= self.target_tokens:
                    current_units = [overlap_text]
                    current_tokens = overlap_tokens_count
                else:
                    current_units = []
                    current_tokens = 0

            current_units.append(unit)
            current_tokens += unit_tokens

        if current_units:
            chunk_text = "\n\n".join(current_units)
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