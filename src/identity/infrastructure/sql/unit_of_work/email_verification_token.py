from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.ports.email_verification_token_command_repository import EmailVerificationTokenCommandRepository
from src.identity.domain.ports.email_verification_token_query_repository import EmailVerificationTokenQueryRepository
from src.identity.infrastructure.sql.email_verification_token_command_repository import SQLAlchemyEmailVerificationTokenCommandRepository
from src.identity.infrastructure.sql.email_verification_token_query_repository import SQLAlchemyEmailVerificationTokenQueryRepository


class SQLAlchemyEmailVerificationTokenUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._query: EmailVerificationTokenQueryRepository | None = None
        self._command: EmailVerificationTokenCommandRepository | None = None

    @property
    def query(self) -> EmailVerificationTokenQueryRepository:
        if self._query is None:
            self._query = SQLAlchemyEmailVerificationTokenQueryRepository(self._session)
        return self._query

    @property
    def command(self) -> EmailVerificationTokenCommandRepository:
        if self._command is None:
            self._command = SQLAlchemyEmailVerificationTokenCommandRepository(self._session)
        return self._command
