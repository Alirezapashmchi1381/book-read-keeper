from dataclasses import dataclass

from src.library.application.dtos.reorder_shelf_dto import ReorderShelfInputDto
from src.library.domain.entities.shelf import Shelf
from src.library.domain.exceptions import ShelfNotFoundError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class ReorderShelfUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, dto: ReorderShelfInputDto) -> Shelf:
        async with self.uow as uow:
            shelf = await uow.shelves.query.find_by_id(dto.shelf_id)
            if shelf is None:
                raise ShelfNotFoundError(f"Shelf {dto.shelf_id} not found")

            shelf.reorder_books(dto.book_ids)
            await uow.shelves.command.save(shelf)
            await uow.commit()
            return shelf