from datetime import datetime
from dataclasses import dataclass, field
from uuid import UUID

from library.domain.value_objects.book_metadata import BookMetadata
from src.library.domain.value_objects.book_file import BookFile
from src.library.domain.value_objects.cover import Cover


@dataclass
class Book:
    id: UUID
    metadata: BookMetadata
    deleted_at: datetime  
    book_file: BookFile | None = None
    cover: Cover | None = None
    is_starred: bool = False
    is_deleted: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
