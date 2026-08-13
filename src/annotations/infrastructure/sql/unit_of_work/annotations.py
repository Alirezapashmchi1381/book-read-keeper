from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.annotations.infrastructure.sql.unit_of_work.base import SQLAlchemyUnitOfWork
from src.annotations.infrastructure.sql.unit_of_work.highlight import SQLAlchemyHighlightUnitOfWork


class SQLAlchemyAnnotationsUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory)
        self._highlights: SQLAlchemyHighlightUnitOfWork | None = None

    @property
    def highlights(self) -> SQLAlchemyHighlightUnitOfWork:
        if self._highlights is None:
            self._highlights = SQLAlchemyHighlightUnitOfWork(self.session)
        return self._highlights

    async def __aenter__(self) -> "SQLAlchemyAnnotationsUnitOfWork":
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
            self._highlights = None