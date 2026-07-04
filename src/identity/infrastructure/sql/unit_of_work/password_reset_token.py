from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.ports.password_reset_token_command_repository import PasswordResetTokenCommandRepository
from src.identity.domain.ports.password_reset_token_query_repository import PasswordResetTokenQueryRepository
from src.identity.infrastructure.sql.password_reset_token_command_repository import SQLAlchemyPasswordResetTokenCommandRepository
from src.identity.infrastructure.sql.password_reset_token_query_repository import SQLAlchemyPasswordResetTokenQueryRepository


class SQLAlchemyPasswordResetTokenUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: PasswordResetTokenQueryRepository | None = None
        self._command: PasswordResetTokenCommandRepository | None = None

    @property
    def query(self) -> PasswordResetTokenQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyPasswordResetTokenQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> PasswordResetTokenCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyPasswordResetTokenCommandRepository(self._session)
        return self._command
