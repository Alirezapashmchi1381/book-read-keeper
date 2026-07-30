from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UploadBookFileInputDto:
    book_id: UUID
    content: bytes
    format: str
    mime_type: str