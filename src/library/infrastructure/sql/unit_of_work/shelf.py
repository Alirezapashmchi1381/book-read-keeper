from sqlalchemy.ext.asyncio import AsyncSession

from src.library.domain.ports.shelf_command_repository import ShelfCommandRepository
from src.library.domain.ports.shelf_query_repository import ShelfQueryRepository
from src.library.infrastructure.sql.repository.sqlalchemy_shelf_command_repository import (
    SQLAlchemyShelfCommandRepository,
)
from src.library.infrastructure.sql.repository.sqlalchemy_shelf_query_repository import (
    SQLAlchemyShelfQueryRepository,
)


class SQLAlchemyShelfUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: ShelfQueryRepository | None = None
        self._command: ShelfCommandRepository | None = None

    @property
    def query(self) -> ShelfQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyShelfQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> ShelfCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyShelfCommandRepository(self._session)
        return self._command