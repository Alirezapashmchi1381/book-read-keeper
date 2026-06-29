from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from src.identity.domain.value_objects.email import Email
from src.identity.domain.value_objects.user_id import UserId


@dataclass
class User():
    id: UserId
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


    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored password hash."""
        # TODO: Implement password verification logic (e.g., using bcrypt or argon2)
        return self.password_hash == password

    @classmethod
    def create(cls, email: Email, username: str, password_hash: str) -> "User":
        return cls(
            id=UserId(uuid4()),
            email=email,
            username=username,
            password_hash=password_hash,
            is_active=True,
            is_verified=False,
        )