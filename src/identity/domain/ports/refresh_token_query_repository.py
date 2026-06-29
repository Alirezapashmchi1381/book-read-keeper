from typing import Optional, Protocol
from uuid import UUID

from src.identity.domain.entities.refresh_token import RefreshToken


class RefreshTokenQueryRepository(Protocol):
    def find_by_id(self, token_id: UUID) -> Optional[RefreshToken]: ...

    def find_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]: ...

    def find_all_by_user_id(self, user_id: UUID) -> list[RefreshToken]: ...
    