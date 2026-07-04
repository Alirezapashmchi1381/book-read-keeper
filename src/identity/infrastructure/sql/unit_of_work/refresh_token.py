from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.ports.refresh_token_command_repository import RefreshTokenCommandRepository
from src.identity.domain.ports.refresh_token_query_repository import RefreshTokenQueryRepository
from src.identity.infrastructure.sql.refresh_token_command_repository import SQLAlchemyRefreshTokenCommandRepository
from src.identity.infrastructure.sql.refresh_token_query_repository import SQLAlchemyRefreshTokenQueryRepository


class SQLAlchemyRefreshTokenUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: RefreshTokenQueryRepository | None = None
        self._command: RefreshTokenCommandRepository | None = None

    @property
    def query(self) -> RefreshTokenQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyRefreshTokenQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> RefreshTokenCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyRefreshTokenCommandRepository(self._session)
        return self._command
