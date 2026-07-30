from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.isbn import ISBN
from src.library.domain.value_objects.language import Language
from src.library.domain.value_objects.color import Color


@dataclass(frozen=True)
class SearchBooksInputDto:
    title: str


@dataclass(frozen=True)
class BookOutputDto:
    id: UUID
    title: str
    author_first_name: str
    author_last_name: str
    isbn: str
    language: str
    color: str
    description: str | None
    is_starred: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime