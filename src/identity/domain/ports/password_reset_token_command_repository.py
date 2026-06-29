from typing import Protocol
from uuid import UUID

from src.identity.domain.entities.password_reset_token import PasswordResetToken


class PasswordResetTokenCommandRepository(Protocol):
    async def save(self, token: PasswordResetToken) -> None: ...

    async def delete(self, token_id: UUID) -> None: ...

    async def delete_all_for_user(self, user_id: UUID) -> None: ...

    async def delete_expired(self) -> None: ...
