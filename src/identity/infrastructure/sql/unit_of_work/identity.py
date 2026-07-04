from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.identity.infrastructure.sql.unit_of_work.base import SQLAlchemyUnitOfWork
from src.identity.infrastructure.sql.unit_of_work.email_verification_token import SQLAlchemyEmailVerificationTokenUnitOfWork
from src.identity.infrastructure.sql.unit_of_work.password_reset_token import SQLAlchemyPasswordResetTokenUnitOfWork
from src.identity.infrastructure.sql.unit_of_work.refresh_token import SQLAlchemyRefreshTokenUnitOfWork
from src.identity.infrastructure.sql.unit_of_work.user import SQLAlchemyUserUnitOfWork


class SQLAlchemyIdentityUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory)
        self._users: SQLAlchemyUserUnitOfWork | None = None
        self._refresh_tokens: SQLAlchemyRefreshTokenUnitOfWork | None = None
        self._email_verification_tokens: SQLAlchemyEmailVerificationTokenUnitOfWork | None = None
        self._password_reset_tokens: SQLAlchemyPasswordResetTokenUnitOfWork | None = None

    @property
    def users(self) -> SQLAlchemyUserUnitOfWork:
        if self._users is None:
            self._users = SQLAlchemyUserUnitOfWork(self.session)
        return self._users

    @property
    def refresh_tokens(self) -> SQLAlchemyRefreshTokenUnitOfWork:
        if self._refresh_tokens is None:
            self._refresh_tokens = SQLAlchemyRefreshTokenUnitOfWork(self.session)
        return self._refresh_tokens

    @property
    def email_verification_tokens(self) -> SQLAlchemyEmailVerificationTokenUnitOfWork:
        if self._email_verification_tokens is None:
            self._email_verification_tokens = SQLAlchemyEmailVerificationTokenUnitOfWork(self.session)
        return self._email_verification_tokens

    @property
    def password_reset_tokens(self) -> SQLAlchemyPasswordResetTokenUnitOfWork:
        if self._password_reset_tokens is None:
            self._password_reset_tokens = SQLAlchemyPasswordResetTokenUnitOfWork(self.session)
        return self._password_reset_tokens

    async def __aenter__(self) -> "SQLAlchemyIdentityUnitOfWork":
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
            self._users = None
            self._refresh_tokens = None
            self._email_verification_tokens = None
            self._password_reset_tokens = None
