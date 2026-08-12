from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.domain.ports.object_command_repository import ObjectCommandRepository
from src.storage.domain.ports.object_query_repository import ObjectQueryRepository
from src.storage.infrastructure.sql.repository.sqlalchemy_object_command_repository import (
    SQLAlchemyObjectCommandRepository,
)
from src.storage.infrastructure.sql.repository.sqlalchemy_object_query_repository import (
    SQLAlchemyObjectQueryRepository,
)


class SQLAlchemyObjectUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: ObjectQueryRepository | None = None
        self._command: ObjectCommandRepository | None = None

    @property
    def query(self) -> ObjectQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyObjectQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> ObjectCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyObjectCommandRepository(self._session)
        return self._command