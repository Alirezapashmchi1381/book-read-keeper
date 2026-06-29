from typing import Protocol

from src.identity.domain.entities.user import User
from src.identity.domain.value_objects.user_id import UserId


class UserCommandRepository(Protocol):
    async def save(self, user: User) -> None: ...

    async def delete(self, user_id: UserId) -> None: ...
