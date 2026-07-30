from dataclasses import dataclass
from uuid import UUID

from src.library.domain.exceptions import ShelfNotFoundError, ShelfNotDeletedError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class RestoreShelfUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, shelf_id: UUID) -> None:
        async with self.uow as uow:
            shelf = await uow.shelves.query.find_by_id(shelf_id)
            if shelf is None:
                raise ShelfNotFoundError(f"Shelf {shelf_id} not found")
            if not shelf.is_deleted:
                raise ShelfNotDeletedError(f"Shelf {shelf_id} is not deleted")

            shelf.restore()
            await uow.shelves.command.save(shelf)
            await uow.commit()