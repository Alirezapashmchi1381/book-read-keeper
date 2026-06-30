from abc import ABC, abstractmethod

from src.identity.domain.ports.email_verification_token_command_repository import EmailVerificationTokenCommandRepository
from src.identity.domain.ports.email_verification_token_query_repository import EmailVerificationTokenQueryRepository
from src.identity.domain.ports.password_reset_token_command_repository import PasswordResetTokenCommandRepository
from src.identity.domain.ports.password_reset_token_query_repository import PasswordResetTokenQueryRepository
from src.identity.domain.ports.refresh_token_command_repository import RefreshTokenCommandRepository
from src.identity.domain.ports.refresh_token_query_repository import RefreshTokenQueryRepository
from src.identity.domain.ports.user_command_repository import UserCommandRepository
from src.identity.domain.ports.user_query_repository import UserQueryRepository


class IdentityUnitOfWork(ABC):
    @property
    @abstractmethod
    def user_query(self) -> UserQueryRepository: ...

    @property
    @abstractmethod
    def user_command(self) -> UserCommandRepository: ...

    @property
    @abstractmethod
    def refresh_token_query(self) -> RefreshTokenQueryRepository: ...

    @property
    @abstractmethod
    def refresh_token_command(self) -> RefreshTokenCommandRepository: ...

    @property
    @abstractmethod
    def password_reset_token_query(self) -> PasswordResetTokenQueryRepository: ...

    @property
    @abstractmethod
    def password_reset_token_command(self) -> PasswordResetTokenCommandRepository: ...

    @property
    @abstractmethod
    def email_verification_token_query(self) -> EmailVerificationTokenQueryRepository: ...

    @property
    @abstractmethod
    def email_verification_token_command(self) -> EmailVerificationTokenCommandRepository: ...

    async def __aenter__(self) -> "IdentityUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
