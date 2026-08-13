from typing import Protocol

from src.reader.domain.ports.reading_session_command_repository import ReadingSessionCommandRepository
from src.reader.domain.ports.reading_session_query_repository import ReadingSessionQueryRepository


class SessionUoW(Protocol):
    query: ReadingSessionQueryRepository
    command: ReadingSessionCommandRepository


class ReaderUnitOfWork(Protocol):
    sessions: SessionUoW

    async def __aenter__(self) -> "ReaderUnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...