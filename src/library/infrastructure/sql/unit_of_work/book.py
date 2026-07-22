from sqlalchemy.ext.asyncio import AsyncSession

from src.library.domain.ports.book_command_repository import BookCommandRepository
from src.library.domain.ports.book_query_repository import BookQueryRepository
from src.library.infrastructure.sql.repository.sqlalchemy_book_command_repository import (
    SQLAlchemyBookCommandRepository,
)
from src.library.infrastructure.sql.repository.sqlalchemy_book_query_repository import (
    SQLAlchemyBookQueryRepository,
)


class SQLAlchemyBookUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: BookQueryRepository | None = None
        self._command: BookCommandRepository | None = None

    @property
    def query(self) -> BookQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyBookQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> BookCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyBookCommandRepository(self._session)
        return self._command