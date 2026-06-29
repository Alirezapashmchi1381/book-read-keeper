from typing import Optional, Protocol

from src.identity.domain.entities.user import User
from src.identity.domain.value_objects.email import Email
from src.identity.domain.value_objects.user_id import UserId


class UserQueryRepository(Protocol):
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...

    def find_by_email(self, email: Email) -> Optional[User]: ...

    def find_by_username(self, username: str) -> Optional[User]: ...

    def exists_by_email(self, email: Email) -> bool: ...

    def exists_by_username(self, username: str) -> bool: ...
