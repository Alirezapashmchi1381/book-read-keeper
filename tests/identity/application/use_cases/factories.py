from datetime import datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

from src.identity.domain.entities.email_verification_token import EmailVerificationToken
from src.identity.domain.entities.password_reset_token import PasswordResetToken
from src.identity.domain.entities.refresh_token import RefreshToken
from src.identity.domain.entities.user import User
from src.identity.domain.value_objects.email import Email


class FakeSubUoW:
    def __init__(self) -> None:
        self.query = AsyncMock()
        self.command = AsyncMock()


class FakeIdentityUnitOfWork:
    def __init__(self) -> None:
        self.users = FakeSubUoW()
        self.refresh_tokens = FakeSubUoW()
        self.email_verification_tokens = FakeSubUoW()
        self.password_reset_tokens = FakeSubUoW()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> "FakeIdentityUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.committed = True
        else:
            self.rolled_back = True

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True


class FakePasswordHasher:
    def hash(self, plain: str) -> str:
        return f"hashed:{plain}"

    def verify(self, plain: str, hashed: str) -> bool:
        return hashed == f"hashed:{plain}"


class FakeTokenHasher:
    def hash(self, token: str) -> str:
        return f"token:{token}"

    def verify(self, token: str, hashed: str) -> bool:
        return hashed == f"token:{token}"


class FakeSecretGenerator:
    def generate(self) -> str:
        return "fake-refresh-token"


class FakeTokenService:
    def generate_access_token(self, user_id) -> str:
        return "fake-access-token"

    def verify_access_token(self, token: str):
        from uuid import UUID
        if token == "fake-access-token":
            return UUID("00000000-0000-0000-0000-000000000001")
        raise ValueError("Invalid or expired access token")


class FakeEmailService:
    def __init__(self) -> None:
        self.sent_verification: list[tuple[str, str]] = []
        self.sent_reset: list[tuple[str, str]] = []

    async def send_email_verification(self, to_email: str, raw_token: str) -> None:
        self.sent_verification.append((to_email, raw_token))

    async def send_password_reset(self, to_email: str, raw_token: str) -> None:
        self.sent_reset.append((to_email, raw_token))


def make_refresh_token(
    user_id=None,
    *,
    raw_token: str = "fake-refresh-token",
    expired: bool = False,
    revoked: bool = False,
) -> RefreshToken:
    hasher = FakeTokenHasher()
    expires_at = datetime.now() + (timedelta(seconds=-1) if expired else timedelta(days=7))
    token = RefreshToken.create(
        user_id=user_id or uuid4(),
        token_hash=hasher.hash(raw_token),
        expires_at=expires_at,
    )
    if revoked:
        token.revoke()
    return token


def make_email_verification_token(
    user_id=None,
    *,
    raw_token: str = "fake-verification-token",
    expired: bool = False,
) -> EmailVerificationToken:
    hasher = FakeTokenHasher()
    expires_at = datetime.now() + (timedelta(seconds=-1) if expired else timedelta(hours=24))
    return EmailVerificationToken.create(
        user_id=user_id or uuid4(),
        token_hash=hasher.hash(raw_token),
        expires_at=expires_at,
    )


def make_password_reset_token(
    user_id=None,
    *,
    raw_token: str = "fake-reset-token",
    expired: bool = False,
) -> PasswordResetToken:
    hasher = FakeTokenHasher()
    expires_at = datetime.now() + (timedelta(seconds=-1) if expired else timedelta(hours=1))
    return PasswordResetToken.create(
        user_id=user_id or uuid4(),
        token_hash=hasher.hash(raw_token),
        expires_at=expires_at,
    )


def make_user(
    *,
    email: str = "user@example.com",
    username: str = "testuser",
    password: str = "secret",
    is_active: bool = True,
    is_verified: bool = False,
) -> User:
    hasher = FakePasswordHasher()
    user = User.create(
        email=Email(email),
        username=username,
        password_hash=hasher.hash(password),
    )
    if not is_active:
        user.deactivate()
    if is_verified:
        user.verify()
    return user
