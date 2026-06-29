from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from typing import Optional


@dataclass
class RefreshToken:
    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    revoked : bool
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def revoke(self):
        self.revoked= True
    def is_expired(self, now: datetime):
        return now >= self.expires_at
    
    def is_valid(self, now: datetime):
        return (not self.revoked) and (not self.is_expired(now))

    @classmethod
    def create(cls, user_id: UUID, token_hash: str, expires_at: datetime) -> "RefreshToken":
        return cls(
            id=uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            revoked=False,
        )