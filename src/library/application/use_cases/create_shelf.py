from dataclasses import dataclass
from uuid import uuid4

from src.library.application.dtos.create_shelf_dto import CreateShelfInputDto
from src.library.domain.entities.shelf import Shelf
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork
from src.library.domain.value_objects.shelf_name import ShelfName
from src.library.domain.value_objects.color import Color


@dataclass
class CreateShelfUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, dto: CreateShelfInputDto) -> Shelf:
        async with self.uow as uow:
            shelf = Shelf(
                id=uuid4(),
                name=ShelfName(dto.name),
                color=Color(dto.color),
            )
            await uow.shelves.command.save(shelf)
            await uow.commit()
            return shelf