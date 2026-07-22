from typing import Protocol
from uuid import UUID

from src.library.domain.entities.shelf import Shelf


class ShelfCommandRepository(Protocol):
    async def save(self, shelf: Shelf) -> None: ...

    async def delete(self, shelf_id: UUID) -> None: ...