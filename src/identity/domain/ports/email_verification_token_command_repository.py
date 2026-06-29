from typing import Protocol
from uuid import UUID

from src.identity.domain.entities.email_verification_token import EmailVerificationToken


class EmailVerificationTokenCommandRepository(Protocol):
    async def save(self, token: EmailVerificationToken) -> None: ...

    async def delete(self, token_id: UUID) -> None: ...

    async def delete_all_for_user(self, user_id: UUID) -> None: ...

    async def delete_expired(self) -> None: ...
