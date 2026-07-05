from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from uuid import UUID

from src.identity.domain.value_objects.email import Email
from src.identity.domain.ports.password_hasher import PasswordHasher

@dataclass
class User():
    id: UUID
    email: Email
    username: str
    password_hash: str
    is_active: bool
    is_verified: bool
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
        self.updated_at = datetime.now()

    def verify(self) -> None:
        """Verify the user account."""
        self.is_verified = True
        self.updated_at = datetime.now()

    @classmethod
    def create(cls, email: Email, username: str, password_hash: str) -> "User":
        return cls(
            id=uuid4(),
            email=email,
            username=username,
            password_hash=password_hash,
            is_active=True,
            is_verified=False,
        )