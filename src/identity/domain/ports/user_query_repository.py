from typing import Optional, Protocol
from uuid import UUID

from src.identity.domain.entities.user import User
from src.identity.domain.value_objects.email import Email


class UserQueryRepository(Protocol):
    async def find_by_id(self, user_id: UUID) -> Optional[User]: ...

    async def find_by_email(self, email: Email) -> Optional[User]: ...

    async def find_by_username(self, username: str) -> Optional[User]: ...

    async def exists_by_email(self, email: Email) -> bool: ...

    async def exists_by_username(self, username: str) -> bool: ...
