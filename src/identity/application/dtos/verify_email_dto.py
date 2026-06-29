from dataclasses import dataclass


@dataclass(frozen=True)
class RequestEmailVerificationInputDto:
    user_id: str


@dataclass(frozen=True)
class VerifyEmailInputDto:
    verification_token: str
