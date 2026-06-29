from dataclasses import dataclass


@dataclass(frozen=True)
class LoginInputDto:
    email: str
    password: str
