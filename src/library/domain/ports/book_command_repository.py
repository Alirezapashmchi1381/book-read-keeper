from typing import Protocol
from uuid import UUID

from src.library.domain.entities.book import Book


class BookCommandRepository(Protocol):
    async def save(self, book: Book) -> None: ...

    async def delete(self, book_id: UUID) -> None: ...