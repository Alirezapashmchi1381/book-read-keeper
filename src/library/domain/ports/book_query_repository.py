from typing import Protocol
from uuid import UUID

from src.library.domain.entities.book import Book


class BookQueryRepository(Protocol):
    async def find_by_id(self, book_id: UUID) -> Book | None: ...

    async def find_by_shelf_id(self, shelf_id: UUID) -> list[Book]: ...

    async def search_by_title(self, title: str) -> list[Book]: ...

    async def find_starred_by_shelf_id(self, shelf_id: UUID) -> list[Book]: ...