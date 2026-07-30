from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddBookToShelfInputDto:
    shelf_id: UUID
    book_id: UUID