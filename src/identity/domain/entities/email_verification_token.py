from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from uuid6 import uuid7


@dataclass
class EmailVerificationToken:
    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    created_at: datetime = field(default_factory=datetime.now)

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at

    @classmethod
    def create(cls, user_id: UUID, token_hash: str, expires_at: datetime) -> "EmailVerificationToken":
        return cls(
            id=uuid7(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
