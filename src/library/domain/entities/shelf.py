from datetime import datetime
from dataclasses import dataclass, field
from uuid import UUID

from src.library.domain.entities.book import Book
from src.library.domain.value_objects.shelf_name import ShelfName
from src.library.domain.value_objects.color import Color


@dataclass
class Shelf:
    id: UUID
    name: ShelfName
    color: Color
    deleted_at: datetime  
    books: list[Book] = field(default_factory=list)
    is_starred: bool = False
    is_deleted: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)