from typing import Protocol

from src.identity.domain.ports.email_verification_token_command_repository import EmailVerificationTokenCommandRepository
from src.identity.domain.ports.email_verification_token_query_repository import EmailVerificationTokenQueryRepository
from src.identity.domain.ports.password_reset_token_command_repository import PasswordResetTokenCommandRepository
from src.identity.domain.ports.password_reset_token_query_repository import PasswordResetTokenQueryRepository
from src.identity.domain.ports.refresh_token_command_repository import RefreshTokenCommandRepository
from src.identity.domain.ports.refresh_token_query_repository import RefreshTokenQueryRepository
from src.identity.domain.ports.user_command_repository import UserCommandRepository
from src.identity.domain.ports.user_query_repository import UserQueryRepository


class IdentityUnitOfWork(Protocol):
    user_query: UserQueryRepository
    user_command: UserCommandRepository
    refresh_token_query: RefreshTokenQueryRepository
    refresh_token_command: RefreshTokenCommandRepository
    password_reset_token_query: PasswordResetTokenQueryRepository
    password_reset_token_command: PasswordResetTokenCommandRepository
    email_verification_token_query: EmailVerificationTokenQueryRepository
    email_verification_token_command: EmailVerificationTokenCommandRepository

    async def __aenter__(self) -> "IdentityUnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
