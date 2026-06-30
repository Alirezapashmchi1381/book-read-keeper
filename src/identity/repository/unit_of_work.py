from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.identity.domain.ports.email_verification_token_command_repository import EmailVerificationTokenCommandRepository
from src.identity.domain.ports.email_verification_token_query_repository import EmailVerificationTokenQueryRepository
from src.identity.domain.ports.password_reset_token_command_repository import PasswordResetTokenCommandRepository
from src.identity.domain.ports.password_reset_token_query_repository import PasswordResetTokenQueryRepository
from src.identity.domain.ports.refresh_token_command_repository import RefreshTokenCommandRepository
from src.identity.domain.ports.refresh_token_query_repository import RefreshTokenQueryRepository
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.ports.user_command_repository import UserCommandRepository
from src.identity.domain.ports.user_query_repository import UserQueryRepository
from src.identity.repository.email_verification_token_command_repository import SQLAlchemyEmailVerificationTokenCommandRepository
from src.identity.repository.email_verification_token_query_repository import SQLAlchemyEmailVerificationTokenQueryRepository
from src.identity.repository.password_reset_token_command_repository import SQLAlchemyPasswordResetTokenCommandRepository
from src.identity.repository.password_reset_token_query_repository import SQLAlchemyPasswordResetTokenQueryRepository
from src.identity.repository.refresh_token_command_repository import SQLAlchemyRefreshTokenCommandRepository
from src.identity.repository.refresh_token_query_repository import SQLAlchemyRefreshTokenQueryRepository
from src.identity.repository.user_command_repository import SQLAlchemyUserCommandRepository
from src.identity.repository.user_query_repository import SQLAlchemyUserQueryRepository


class SQLAlchemyIdentityUnitOfWork(IdentityUnitOfWork):
    """
    Opens one AsyncSession per `async with` block and lazily constructs
    repository instances so they all share the same session.
    Cache is cleared after every commit/rollback so the object is safe
    to reuse across multiple transactions (one per request in practice).
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._user_query: UserQueryRepository | None = None
        self._user_command: UserCommandRepository | None = None
        self._refresh_token_query: RefreshTokenQueryRepository | None = None
        self._refresh_token_command: RefreshTokenCommandRepository | None = None
        self._password_reset_token_query: PasswordResetTokenQueryRepository | None = None
        self._password_reset_token_command: PasswordResetTokenCommandRepository | None = None
        self._email_verification_token_query: EmailVerificationTokenQueryRepository | None = None
        self._email_verification_token_command: EmailVerificationTokenCommandRepository | None = None

    # ------------------------------------------------------------------
    # Repository accessors — lazy, cached per transaction
    # ------------------------------------------------------------------

    @property
    def user_query(self) -> UserQueryRepository:
        if self._user_query is None:
            self._user_query = SQLAlchemyUserQueryRepository(self._session_or_raise())
        return self._user_query

    @property
    def user_command(self) -> UserCommandRepository:
        if self._user_command is None:
            self._user_command = SQLAlchemyUserCommandRepository(self._session_or_raise())
        return self._user_command

    @property
    def refresh_token_query(self) -> RefreshTokenQueryRepository:
        if self._refresh_token_query is None:
            self._refresh_token_query = SQLAlchemyRefreshTokenQueryRepository(self._session_or_raise())
        return self._refresh_token_query

    @property
    def refresh_token_command(self) -> RefreshTokenCommandRepository:
        if self._refresh_token_command is None:
            self._refresh_token_command = SQLAlchemyRefreshTokenCommandRepository(self._session_or_raise())
        return self._refresh_token_command

    @property
    def password_reset_token_query(self) -> PasswordResetTokenQueryRepository:
        if self._password_reset_token_query is None:
            self._password_reset_token_query = SQLAlchemyPasswordResetTokenQueryRepository(self._session_or_raise())
        return self._password_reset_token_query

    @property
    def password_reset_token_command(self) -> PasswordResetTokenCommandRepository:
        if self._password_reset_token_command is None:
            self._password_reset_token_command = SQLAlchemyPasswordResetTokenCommandRepository(self._session_or_raise())
        return self._password_reset_token_command

    @property
    def email_verification_token_query(self) -> EmailVerificationTokenQueryRepository:
        if self._email_verification_token_query is None:
            self._email_verification_token_query = SQLAlchemyEmailVerificationTokenQueryRepository(self._session_or_raise())
        return self._email_verification_token_query

    @property
    def email_verification_token_command(self) -> EmailVerificationTokenCommandRepository:
        if self._email_verification_token_command is None:
            self._email_verification_token_command = SQLAlchemyEmailVerificationTokenCommandRepository(self._session_or_raise())
        return self._email_verification_token_command

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "SQLAlchemyIdentityUnitOfWork":
        self._session = self._session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self._session_or_raise().close()
            self._evict_cache()

    # ------------------------------------------------------------------
    # Explicit transaction control
    # ------------------------------------------------------------------

    async def commit(self) -> None:
        await self._session_or_raise().commit()

    async def rollback(self) -> None:
        await self._session_or_raise().rollback()

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _session_or_raise(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError(
                "No active session. Use 'async with uow' before accessing repositories."
            )
        return self._session

    def _evict_cache(self) -> None:
        self._session = None
        self._user_query = None
        self._user_command = None
        self._refresh_token_query = None
        self._refresh_token_command = None
        self._password_reset_token_query = None
        self._password_reset_token_command = None
        self._email_verification_token_query = None
        self._email_verification_token_command = None
