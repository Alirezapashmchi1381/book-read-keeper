from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.storage.infrastructure.sql.unit_of_work.base import SQLAlchemyUnitOfWork
from src.storage.infrastructure.sql.unit_of_work.object import SQLAlchemyObjectUnitOfWork


class SQLAlchemyStorageUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory)
        self._objects: SQLAlchemyObjectUnitOfWork | None = None

    @property
    def objects(self) -> SQLAlchemyObjectUnitOfWork:
        if self._objects is None:
            self._objects = SQLAlchemyObjectUnitOfWork(self.session)
        return self._objects

    async def __aenter__(self) -> "SQLAlchemyStorageUnitOfWork":
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
            self._objects = None