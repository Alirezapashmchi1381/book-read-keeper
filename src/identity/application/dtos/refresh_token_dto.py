from dataclasses import dataclass


@dataclass(frozen=True)
class RefreshTokenInputDto:
    refresh_token: str


@dataclass(frozen=True)
class RefreshTokenResultDto:
    access_token: str
    refresh_token: str
