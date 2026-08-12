from pydantic import BaseModel
from typing import Optional


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    token_count: int
    page_number: Optional[int] = None
    section: Optional[str] = None