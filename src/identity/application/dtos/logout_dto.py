from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class LogoutInputDto:
    refresh_token: str


@dataclass(frozen=True)
class LogoutAllDevicesInputDto:
    user_id: UUID
