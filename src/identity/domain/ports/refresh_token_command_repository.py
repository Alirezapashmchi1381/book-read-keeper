from typing import Protocol
from uuid import UUID

from src.identity.domain.entities.refresh_token import RefreshToken


class RefreshTokenCommandRepository(Protocol):
    def save(self, token: RefreshToken) -> None: ...

    def revoke(self, token_id: UUID) -> None: ...

    def revoke_all_for_user(self, user_id: UUID) -> None: ...

    def delete_expired(self) -> None: ...
