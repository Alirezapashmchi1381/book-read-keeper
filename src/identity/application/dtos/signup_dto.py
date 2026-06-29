from dataclasses import dataclass


@dataclass(frozen=True)
class SignupInputDto:
    email: str
    username: str
    password: str
