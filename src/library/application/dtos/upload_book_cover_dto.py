from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UploadBookCoverInputDto:
    book_id: UUID
    content: bytes
    mime_type: str