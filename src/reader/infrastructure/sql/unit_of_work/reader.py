from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.reader.infrastructure.sql.unit_of_work.base import SQLAlchemyUnitOfWork
from src.reader.infrastructure.sql.unit_of_work.session import SQLAlchemySessionUnitOfWork


class SQLAlchemyReaderUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory)
        self._sessions: SQLAlchemySessionUnitOfWork | None = None

    @property
    def sessions(self) -> SQLAlchemySessionUnitOfWork:
        if self._sessions is None:
            self._sessions = SQLAlchemySessionUnitOfWork(self.session)
        return self._sessions

    async def __aenter__(self) -> "SQLAlchemyReaderUnitOfWork":
        await super().__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        try:
            await super().__aexit__(exc_type, exc_val, exc_tb)
        finally:
            self._sessions = None