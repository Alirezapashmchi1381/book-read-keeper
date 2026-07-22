from typing import Protocol
from uuid import UUID

from src.library.domain.entities.shelf import Shelf


class ShelfQueryRepository(Protocol):
    async def find_by_id(self, shelf_id: UUID) -> Shelf | None: ...

    async def list_all(self) -> list[Shelf]: ...

    async def find_starred(self) -> list[Shelf]: ...