from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Embed a single piece of text. Returns a vector as a list of floats."""
        ...

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts. Returns a list of vectors, same order as input."""
        ...