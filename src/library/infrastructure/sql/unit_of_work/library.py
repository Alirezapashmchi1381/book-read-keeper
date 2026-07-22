from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.library.infrastructure.sql.unit_of_work import SQLAlchemyUnitOfWork
from src.library.infrastructure.sql.unit_of_work.book import SQLAlchemyBookUnitOfWork
from src.library.infrastructure.sql.unit_of_work.shelf import SQLAlchemyShelfUnitOfWork


class SQLAlchemyLibraryUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory)
        self._books: SQLAlchemyBookUnitOfWork | None = None
        self._shelves: SQLAlchemyShelfUnitOfWork | None = None

    @property
    def books(self) -> SQLAlchemyBookUnitOfWork:
        if self._books is None:
            self._books = SQLAlchemyBookUnitOfWork(self.session)
        return self._books

    @property
    def shelves(self) -> SQLAlchemyShelfUnitOfWork:
        if self._shelves is None:
            self._shelves = SQLAlchemyShelfUnitOfWork(self.session)
        return self._shelves

    async def __aenter__(self) -> "SQLAlchemyLibraryUnitOfWork":
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
            self._books = None
            self._shelves = None