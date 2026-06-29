from typing import Optional, Protocol

from src.identity.domain.entities.password_reset_token import PasswordResetToken


class PasswordResetTokenQueryRepository(Protocol):
    async def find_by_token_hash(self, token_hash: str) -> Optional[PasswordResetToken]: ...
