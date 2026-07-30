from dataclasses import dataclass

from src.library.application.dtos.shelf_output_dto import ShelfOutputDto
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class ListShelvesUseCase:
    uow: LibraryUnitOfWork

    async def execute(self) -> list[ShelfOutputDto]:
        async with self.uow as uow:
            shelves = await uow.shelves.query.list_all()

        return [
            ShelfOutputDto(
                id=shelf.id,
                name=shelf.name.name,
                color=shelf.color.hex_value,
                book_count=shelf.book_count(),
                is_starred=shelf.is_starred,
                is_deleted=shelf.is_deleted,
                created_at=shelf.created_at,
                updated_at=shelf.updated_at,
            )
            for shelf in shelves
        ]