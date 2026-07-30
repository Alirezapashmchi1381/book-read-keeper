from dataclasses import dataclass
from uuid import UUID

from src.library.domain.exceptions import ShelfNotFoundError, ShelfAlreadyDeletedError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class DeleteShelfUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, shelf_id: UUID) -> None:
        async with self.uow as uow:
            shelf = await uow.shelves.query.find_by_id(shelf_id)
            if shelf is None:
                raise ShelfNotFoundError(f"Shelf {shelf_id} not found")
            if shelf.is_deleted:
                raise ShelfAlreadyDeletedError(f"Shelf {shelf_id} is already deleted")

            shelf.soft_delete()
            await uow.shelves.command.save(shelf)
            await uow.commit()