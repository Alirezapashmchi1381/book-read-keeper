from dataclasses import dataclass


@dataclass(frozen=True)
class RequestPasswordResetInputDto:
    email: str
