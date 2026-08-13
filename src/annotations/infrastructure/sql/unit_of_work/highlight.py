from sqlalchemy.ext.asyncio import AsyncSession

from src.annotations.domain.ports.highlight_command_repository import HighlightCommandRepository
from src.annotations.domain.ports.highlight_query_repository import HighlightQueryRepository
from src.annotations.infrastructure.sql.repository.sqlalchemy_highlight_command_repository import (
    SQLAlchemyHighlightCommandRepository,
)
from src.annotations.infrastructure.sql.repository.sqlalchemy_highlight_query_repository import (
    SQLAlchemyHighlightQueryRepository,
)


class SQLAlchemyHighlightUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: HighlightQueryRepository | None = None
        self._command: HighlightCommandRepository | None = None

    @property
    def query(self) -> HighlightQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyHighlightQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> HighlightCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyHighlightCommandRepository(self._session)
        return self._command