from dataclasses import dataclass


@dataclass(frozen=True)
class ResetPasswordInputDto:
    reset_token: str
    new_password: str
