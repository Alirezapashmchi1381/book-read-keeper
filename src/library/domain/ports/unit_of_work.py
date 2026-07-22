from typing import Protocol

from src.library.domain.ports.book_command_repository import BookCommandRepository
from src.library.domain.ports.book_query_repository import BookQueryRepository
from src.library.domain.ports.shelf_command_repository import ShelfCommandRepository
from src.library.domain.ports.shelf_query_repository import ShelfQueryRepository


class BookUoW(Protocol):
    query: BookQueryRepository
    command: BookCommandRepository


class ShelfUoW(Protocol):
    query: ShelfQueryRepository
    command: ShelfCommandRepository


class LibraryUnitOfWork(Protocol):
    books: BookUoW
    shelves: ShelfUoW

    async def __aenter__(self) -> "LibraryUnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...