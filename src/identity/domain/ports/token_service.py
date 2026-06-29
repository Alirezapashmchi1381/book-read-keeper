from typing import Protocol
from uuid import UUID


class TokenService(Protocol):
    def generate_access_token(self, user_id: UUID) -> str: ...

    def generate_refresh_token(self) -> str: ...
