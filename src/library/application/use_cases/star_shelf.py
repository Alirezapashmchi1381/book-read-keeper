from dataclasses import dataclass
from uuid import UUID

from src.library.domain.entities.shelf import Shelf
from src.library.domain.exceptions import ShelfNotFoundError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class StarShelfUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, shelf_id: UUID) -> Shelf:
        async with self.uow as uow:
            shelf = await uow.shelves.query.find_by_id(shelf_id)
            if shelf is None:
                raise ShelfNotFoundError(f"Shelf {shelf_id} not found")

            shelf.toggle_star()
            await uow.shelves.command.save(shelf)
            await uow.commit()
            return shelf