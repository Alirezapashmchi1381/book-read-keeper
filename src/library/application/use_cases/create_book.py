from dataclasses import dataclass

from src.library.application.dtos.create_book_dto import CreateBookInputDto
from src.library.domain.entities.book import Book
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class CreateBookUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, dto: CreateBookInputDto) -> Book:
        async with self.uow as uow:
            book = Book.create(dto.to_metadata())
            await uow.books.command.save(book)
            await uow.commit()
            return book