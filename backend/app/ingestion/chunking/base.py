from abc import ABC, abstractmethod
from app.models.chunk import Chunk


class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, text: str, document_id: str) -> list[Chunk]:
        """Split text into a list of Chunk objects."""
        ...