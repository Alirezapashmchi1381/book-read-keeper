from dataclasses import dataclass
from uuid import UUID

from src.library.domain.entities.book import Book
from src.library.domain.exceptions import BookNotFoundError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class GetBookUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, book_id: UUID) -> Book:
        async with self.uow as uow:
            book = await uow.books.query.find_by_id(book_id)
            if book is None:
                raise BookNotFoundError(f"Book {book_id} not found")
            return book