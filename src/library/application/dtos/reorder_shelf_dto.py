from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ReorderShelfInputDto:
    shelf_id: UUID
    book_ids: list[UUID]