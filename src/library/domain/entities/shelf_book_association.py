from dataclasses import dataclass
from uuid import UUID


@dataclass
class ShelfBookAssociation:
    shelf_id: UUID
    book_id: UUID
    position: int = 0