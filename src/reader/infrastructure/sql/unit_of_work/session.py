from sqlalchemy.ext.asyncio import AsyncSession

from src.reader.domain.ports.reading_session_command_repository import ReadingSessionCommandRepository
from src.reader.domain.ports.reading_session_query_repository import ReadingSessionQueryRepository
from src.reader.infrastructure.sql.repository.sqlalchemy_reading_session_command_repository import (
    SQLAlchemyReadingSessionCommandRepository,
)
from src.reader.infrastructure.sql.repository.sqlalchemy_reading_session_query_repository import (
    SQLAlchemyReadingSessionQueryRepository,
)


class SQLAlchemySessionUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: ReadingSessionQueryRepository | None = None
        self._command: ReadingSessionCommandRepository | None = None

    @property
    def query(self) -> ReadingSessionQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyReadingSessionQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> ReadingSessionCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyReadingSessionCommandRepository(self._session)
        return self._command