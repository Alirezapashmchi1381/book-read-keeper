from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.identity.application.use_cases.change_password import ChangePasswordUseCase
from src.identity.application.use_cases.deactivate_account import DeactivateAccountUseCase
from src.identity.application.use_cases.login import LoginUseCase
from src.identity.application.use_cases.logout import LogoutUseCase
from src.identity.application.use_cases.logout_all_devices import LogoutAllDevicesUseCase
from src.identity.application.use_cases.refresh_token import RefreshTokenUseCase
from src.identity.application.use_cases.request_email_verification import RequestEmailVerificationUseCase
from src.identity.application.use_cases.request_password_reset import RequestPasswordResetUseCase
from src.identity.application.use_cases.reset_password import ResetPasswordUseCase
from src.identity.application.use_cases.signup import SignupUseCase
from src.identity.application.use_cases.verify_email import VerifyEmailUseCase
from src.identity.domain.ports.email_service import EmailService
from src.identity.infrastructure.password_hasher import Argon2PasswordHasher
from src.identity.infrastructure.token_service import RS256TokenService
from identity.infrastructure.repository.unit_of_work import SQLAlchemyIdentityUnitOfWork


class _UnimplementedEmailService:
    async def send_password_reset(self, to_email: str, raw_token: str) -> None:
        raise NotImplementedError("EmailService is not configured")

    async def send_email_verification(self, to_email: str, raw_token: str) -> None:
        raise NotImplementedError("EmailService is not configured")


_email_service: EmailService = _UnimplementedEmailService()

# ------------------------------------------------------------------
# Infrastructure singletons -- created once at app startup.
# In production, pull the URL from settings / env.
# ------------------------------------------------------------------

_engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/dbname",
    pool_pre_ping=True,
)

_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    _engine,
    expire_on_commit=False,
)

# ------------------------------------------------------------------
# Concrete service singletons.
# Replace with your real implementations when you write them.
# ------------------------------------------------------------------

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

_bearer = HTTPBearer()

# from src.identity.infrastructure.email_service import SmtpEmailService

_password_hasher = Argon2PasswordHasher()

# Load RSA keys from PEM files (paths via env / settings in production).
# Generate with: openssl genrsa -out private.pem 2048
#                openssl rsa -in private.pem -pubout -out public.pem
with open("private.pem", "rb") as f:
    _private_key: RSAPrivateKey = load_pem_private_key(f.read(), password=None)  # type: ignore[assignment]
with open("public.pem", "rb") as f:
    _public_key: RSAPublicKey = load_pem_public_key(f.read())  # type: ignore[assignment]

_token_service = RS256TokenService(
    private_key=_private_key,
    public_key=_public_key,
    issuer="book-read-keeper",
)
# _email_service = SmtpEmailService(...)

# ------------------------------------------------------------------
# UoW factory -- one fresh UoW per use-case execution
# ------------------------------------------------------------------

def _uow_factory() -> SQLAlchemyIdentityUnitOfWork:
    return SQLAlchemyIdentityUnitOfWork(_session_factory)


# ------------------------------------------------------------------
# Per-request use-case providers
# ------------------------------------------------------------------

def get_signup_use_case() -> SignupUseCase:
    return SignupUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
        token_service=_token_service,
    )


def get_login_use_case() -> LoginUseCase:
    return LoginUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
        token_service=_token_service,
    )


def get_logout_use_case() -> LogoutUseCase:
    return LogoutUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
    )


def get_logout_all_devices_use_case() -> LogoutAllDevicesUseCase:
    return LogoutAllDevicesUseCase(
        uow_factory=_uow_factory,
    )


def get_refresh_token_use_case() -> RefreshTokenUseCase:
    return RefreshTokenUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
        token_service=_token_service,
    )


def get_change_password_use_case() -> ChangePasswordUseCase:
    return ChangePasswordUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
    )


def get_deactivate_account_use_case() -> DeactivateAccountUseCase:
    return DeactivateAccountUseCase(
        uow_factory=_uow_factory,
    )


def get_request_password_reset_use_case() -> RequestPasswordResetUseCase:
    return RequestPasswordResetUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
        token_service=_token_service,
        email_service=_email_service,
    )


def get_reset_password_use_case() -> ResetPasswordUseCase:
    return ResetPasswordUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
    )


def get_request_email_verification_use_case() -> RequestEmailVerificationUseCase:
    return RequestEmailVerificationUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
        token_service=_token_service,
        email_service=_email_service,
    )


def get_verify_email_use_case() -> VerifyEmailUseCase:
    return VerifyEmailUseCase(
        uow_factory=_uow_factory,
        password_hasher=_password_hasher,
    )


# ------------------------------------------------------------------
# Auth dependency -- extracts and validates the Bearer JWT
# ------------------------------------------------------------------

def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> UUID:
    try:
        payload = _token_service.decode_access_token(credentials.credentials)
        return UUID(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentUserDep = Annotated[UUID, Depends(get_current_user)]


# ------------------------------------------------------------------
# Annotated dependency aliases for use in route signatures
# ------------------------------------------------------------------

SignupUseCaseDep = Annotated[SignupUseCase, Depends(get_signup_use_case)]
LoginUseCaseDep = Annotated[LoginUseCase, Depends(get_login_use_case)]
LogoutUseCaseDep = Annotated[LogoutUseCase, Depends(get_logout_use_case)]
LogoutAllDevicesUseCaseDep = Annotated[LogoutAllDevicesUseCase, Depends(get_logout_all_devices_use_case)]
RefreshTokenUseCaseDep = Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)]
ChangePasswordUseCaseDep = Annotated[ChangePasswordUseCase, Depends(get_change_password_use_case)]
DeactivateAccountUseCaseDep = Annotated[DeactivateAccountUseCase, Depends(get_deactivate_account_use_case)]
RequestPasswordResetUseCaseDep = Annotated[RequestPasswordResetUseCase, Depends(get_request_password_reset_use_case)]
ResetPasswordUseCaseDep = Annotated[ResetPasswordUseCase, Depends(get_reset_password_use_case)]
RequestEmailVerificationUseCaseDep = Annotated[RequestEmailVerificationUseCase, Depends(get_request_email_verification_use_case)]
VerifyEmailUseCaseDep = Annotated[VerifyEmailUseCase, Depends(get_verify_email_use_case)]
