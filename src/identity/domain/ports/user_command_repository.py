from typing import Protocol
from uuid import UUID

from src.identity.domain.entities.user import User


class UserCommandRepository(Protocol):
    async def save(self, user: User) -> None: ...

    async def delete(self, user_id: UUID) -> None: ...
