from dataclasses import dataclass
from uuid import UUID

from src.library.domain.exceptions import BookNotFoundError, BookNotDeletedError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class RestoreBookUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, book_id: UUID) -> None:
        async with self.uow as uow:
            book = await uow.books.query.find_by_id(book_id)
            if book is None:
                raise BookNotFoundError(f"Book {book_id} not found")
            if not book.is_deleted:
                raise BookNotDeletedError(f"Book {book_id} is not deleted")

            book.restore()
            await uow.books.command.save(book)
            await uow.commit()