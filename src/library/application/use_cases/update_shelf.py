from dataclasses import dataclass

from src.library.application.dtos.update_shelf_dto import UpdateShelfInputDto
from src.library.domain.entities.shelf import Shelf
from src.library.domain.exceptions import ShelfNotFoundError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork
from src.library.domain.value_objects.shelf_name import ShelfName
from src.library.domain.value_objects.color import Color


@dataclass
class UpdateShelfUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, dto: UpdateShelfInputDto) -> Shelf:
        async with self.uow as uow:
            shelf = await uow.shelves.query.find_by_id(dto.shelf_id)
            if shelf is None:
                raise ShelfNotFoundError(f"Shelf {dto.shelf_id} not found")

            if dto.name is not None:
                shelf.rename(ShelfName(dto.name))
            if dto.color is not None:
                shelf.change_color(Color(dto.color))

            await uow.shelves.command.save(shelf)
            await uow.commit()
            return shelf