from typing import Optional, Protocol

from src.identity.domain.entities.email_verification_token import EmailVerificationToken


class EmailVerificationTokenQueryRepository(Protocol):
    async def find_by_token_hash(self, token_hash: str) -> Optional[EmailVerificationToken]: ...
