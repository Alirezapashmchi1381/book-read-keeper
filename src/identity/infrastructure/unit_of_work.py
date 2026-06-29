from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.identity.domain.ports.refresh_token_command_repository import RefreshTokenCommandRepository
from src.identity.domain.ports.refresh_token_query_repository import RefreshTokenQueryRepository
from src.identity.domain.ports.user_command_repository import UserCommandRepository
from src.identity.domain.ports.user_query_repository import UserQueryRepository

# These will be created when the concrete repository modules are written.
from src.identity.repository.user_query_repository import SQLAlchemyUserQueryRepository
from src.identity.repository.user_command_repository import SQLAlchemyUserCommandRepository
from src.identity.repository.refresh_token_query_repository import SQLAlchemyRefreshTokenQueryRepository
from src.identity.repository.refresh_token_command_repository import SQLAlchemyRefreshTokenCommandRepository


class SQLAlchemyIdentityUnitOfWork:
    """
    Opens one AsyncSession per `async with` block and lazily constructs
    repository instances on first access so they all share the same session.
    The cache is cleared after every commit/rollback so the object can be
    reused across multiple transactions (one per request in practice).
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._user_query: UserQueryRepository | None = None
        self._user_command: UserCommandRepository | None = None
        self._refresh_token_query: RefreshTokenQueryRepository | None = None
        self._refresh_token_command: RefreshTokenCommandRepository | None = None

    # ------------------------------------------------------------------
    # Repository accessors -- lazy, cached per transaction
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
