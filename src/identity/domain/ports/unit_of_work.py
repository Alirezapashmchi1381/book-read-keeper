from typing import Protocol

from src.identity.domain.ports.email_verification_token_command_repository import EmailVerificationTokenCommandRepository
from src.identity.domain.ports.email_verification_token_query_repository import EmailVerificationTokenQueryRepository
from src.identity.domain.ports.password_reset_token_command_repository import PasswordResetTokenCommandRepository
from src.identity.domain.ports.password_reset_token_query_repository import PasswordResetTokenQueryRepository
from src.identity.domain.ports.refresh_token_command_repository import RefreshTokenCommandRepository
from src.identity.domain.ports.refresh_token_query_repository import RefreshTokenQueryRepository
from src.identity.domain.ports.user_command_repository import UserCommandRepository
from src.identity.domain.ports.user_query_repository import UserQueryRepository


class UserUoW(Protocol):
    query: UserQueryRepository
    command: UserCommandRepository


class RefreshTokenUoW(Protocol):
    query: RefreshTokenQueryRepository
    command: RefreshTokenCommandRepository


class EmailVerificationTokenUoW(Protocol):
    query: EmailVerificationTokenQueryRepository
    command: EmailVerificationTokenCommandRepository


class PasswordResetTokenUoW(Protocol):
    query: PasswordResetTokenQueryRepository
    command: PasswordResetTokenCommandRepository


class IdentityUnitOfWork(Protocol):
    users: UserUoW
    refresh_tokens: RefreshTokenUoW
    email_verification_tokens: EmailVerificationTokenUoW
    password_reset_tokens: PasswordResetTokenUoW

    async def __aenter__(self) -> "IdentityUnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
