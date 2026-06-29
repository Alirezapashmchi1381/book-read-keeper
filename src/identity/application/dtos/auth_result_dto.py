from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AuthResultDto:
    access_token: str
    refresh_token: str
    user_id: UUID
    username: str
    email: str
