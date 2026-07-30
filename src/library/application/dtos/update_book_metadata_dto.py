from dataclasses import dataclass
from uuid import UUID

from src.library.domain.value_objects.book_metadata import BookMetadata
from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.isbn import ISBN
from src.library.domain.value_objects.language import Language
from src.library.domain.value_objects.color import Color


@dataclass(frozen=True)
class UpdateBookMetadataInputDto:
    book_id: UUID
    author_first_name: str | None = None
    author_last_name: str | None = None
    isbn: str | None = None
    title: str | None = None
    language: str | None = None
    color: str | None = None
    description: str | None = None
    is_starred: bool | None = None