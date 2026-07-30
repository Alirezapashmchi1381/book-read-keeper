from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateShelfInputDto:
    shelf_id: UUID
    name: str | None = None
    color: str | None = None