from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.ports.user_command_repository import UserCommandRepository
from src.identity.domain.ports.user_query_repository import UserQueryRepository
from src.identity.infrastructure.sql.user_command_repository import SQLAlchemyUserCommandRepository
from src.identity.infrastructure.sql.user_query_repository import SQLAlchemyUserQueryRepository


class SQLAlchemyUserUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: UserQueryRepository | None = None
        self._command: UserCommandRepository | None = None

    @property
    def query(self) -> UserQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyUserQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> UserCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyUserCommandRepository(self._session)
        return self._command
