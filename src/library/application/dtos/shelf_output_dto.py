from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.library.domain.value_objects.shelf_name import ShelfName
from src.library.domain.value_objects.color import Color
from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.isbn import ISBN


@dataclass(frozen=True)
class ShelfOutputDto:
    id: UUID
    name: str
    color: str
    book_count: int
    is_starred: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ShelfBookOutputDto:
    id: UUID
    title: str
    author_first_name: str
    author_last_name: str
    isbn: str
    position: int
    is_starred: bool