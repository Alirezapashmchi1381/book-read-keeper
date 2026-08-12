from typing import Protocol

from src.annotations.domain.ports.highlight_command_repository import HighlightCommandRepository
from src.annotations.domain.ports.highlight_query_repository import HighlightQueryRepository


class HighlightUoW(Protocol):
    query: HighlightQueryRepository
    command: HighlightCommandRepository


class AnnotationsUnitOfWork(Protocol):
    highlights: HighlightUoW

    async def __aenter__(self) -> "AnnotationsUnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...