from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from uuid import UUID

from src.identity.domain.exceptions import AuthenticationError
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
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def change_password(self, hasher: PasswordHasher, current: str, new: str) -> None:
        """Verify current password and set a new one.

        Raises AuthenticationError if the current password is incorrect.
        """
        if not hasher.verify(current, self.password_hash):
            raise AuthenticationError("Current password is incorrect")
        self.password_hash = hasher.hash(new)
        self.updated_at = datetime.now(timezone.utc)

    def reset_password(self, hasher: PasswordHasher, new: str) -> None:
        """Set a new password without verifying the old one (used in password reset flow)."""
        self.password_hash = hasher.hash(new)
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)

    def verify(self) -> None:
        """Verify the user account."""
        self.is_verified = True
        self.updated_at = datetime.now(timezone.utc)

    def verify_password(self, plain_password: str, password_hasher: PasswordHasher) -> bool:
        return password_hasher.verify(plain_password, self.password_hash)

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
