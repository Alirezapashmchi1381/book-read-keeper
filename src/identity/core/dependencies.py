from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.config import Settings, get_settings
from src.shared.auth.dependencies import get_current_user_id  # noqa: F401 – re-exported for convenience
from src.core.dependencies.database import get_session_factory
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
from src.identity.infrastructure.services.bcrypt_password_hasher import BcryptPasswordHasher
from src.identity.infrastructure.services.hmac_token_hasher import HMACTokenHasher
from src.identity.infrastructure.services.jwt_token_service import JWTTokenService
from src.identity.infrastructure.services.secrets_generator import SecretsGenerator
from src.identity.infrastructure.services.stub_email_service import StubEmailService
from src.identity.infrastructure.sql.unit_of_work import SQLAlchemyIdentityUnitOfWork

# ---------------------------------------------------------------------------
# Infrastructure layer
# ---------------------------------------------------------------------------

def get_identity_uow(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> SQLAlchemyIdentityUnitOfWork:
    return SQLAlchemyIdentityUnitOfWork(session_factory)


def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()


def get_token_hasher(settings: Settings = Depends(get_settings)) -> HMACTokenHasher:
    return HMACTokenHasher(secret=settings.token_secret)


def get_token_service(settings: Settings = Depends(get_settings)) -> JWTTokenService:
    return JWTTokenService(
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.jwt_access_token_expire_minutes,
    )


def get_secret_generator() -> SecretsGenerator:
    return SecretsGenerator()


def get_email_service() -> StubEmailService:
    return StubEmailService()


# Annotated aliases — use these in router signatures for brevity
IdentityUoWDep = Annotated[SQLAlchemyIdentityUnitOfWork, Depends(get_identity_uow)]
PasswordHasherDep = Annotated[BcryptPasswordHasher, Depends(get_password_hasher)]
TokenHasherDep = Annotated[HMACTokenHasher, Depends(get_token_hasher)]
TokenServiceDep = Annotated[JWTTokenService, Depends(get_token_service)]
SecretGeneratorDep = Annotated[SecretsGenerator, Depends(get_secret_generator)]
EmailServiceDep = Annotated[StubEmailService, Depends(get_email_service)]

# ---------------------------------------------------------------------------
# Use-case providers — one function per use case
# ---------------------------------------------------------------------------

def get_signup_use_case(
    uow: IdentityUoWDep,
    hasher: PasswordHasherDep,
    token_hasher: TokenHasherDep,
    tokens: TokenServiceDep,
    secrets: SecretGeneratorDep,
) -> SignupUseCase:
    return SignupUseCase(
        uow=uow, # type: ignore
        password_hasher=hasher,
        token_hasher=token_hasher,
        token_service=tokens,
        secret_generator=secrets,
    )


def get_login_use_case(
    uow: IdentityUoWDep,
    hasher: PasswordHasherDep,
    token_hasher: TokenHasherDep,
    tokens: TokenServiceDep,
    secrets: SecretGeneratorDep,
) -> LoginUseCase:
    return LoginUseCase(
        uow=uow, # type: ignore
        password_hasher=hasher,
        token_hasher=token_hasher,
        token_service=tokens,
        secret_generator=secrets,
    )


def get_logout_use_case(
    uow: IdentityUoWDep,
    token_hasher: TokenHasherDep,
) -> LogoutUseCase:
    return LogoutUseCase(uow=uow, token_hasher=token_hasher) # type: ignore


def get_logout_all_devices_use_case(uow: IdentityUoWDep) -> LogoutAllDevicesUseCase:
    return LogoutAllDevicesUseCase(uow=uow) # type: ignore


def get_refresh_token_use_case(
    uow: IdentityUoWDep,
    token_hasher: TokenHasherDep,
    tokens: TokenServiceDep,
    secrets: SecretGeneratorDep,
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(
        uow=uow, # type: ignore
        token_hasher=token_hasher,
        token_service=tokens,
        secret_generator=secrets,
    )


def get_change_password_use_case(
    uow: IdentityUoWDep,
    hasher: PasswordHasherDep,
) -> ChangePasswordUseCase:
    return ChangePasswordUseCase(uow=uow, password_hasher=hasher) # type: ignore


def get_deactivate_account_use_case(uow: IdentityUoWDep) -> DeactivateAccountUseCase:
    return DeactivateAccountUseCase(uow=uow) # type: ignore 


def get_request_email_verification_use_case(
    uow: IdentityUoWDep,
    token_hasher: TokenHasherDep,
    secrets: SecretGeneratorDep,
    email: EmailServiceDep,
) -> RequestEmailVerificationUseCase:
    return RequestEmailVerificationUseCase(
        uow=uow, # type: ignore
        token_hasher=token_hasher,
        secret_generator=secrets,
        email_service=email,
    )


def get_verify_email_use_case(
    uow: IdentityUoWDep,
    token_hasher: TokenHasherDep,
) -> VerifyEmailUseCase:
    return VerifyEmailUseCase(uow=uow, token_hasher=token_hasher) # type: ignore


def get_request_password_reset_use_case(
    uow: IdentityUoWDep,
    token_hasher: TokenHasherDep,
    secrets: SecretGeneratorDep,
    email: EmailServiceDep,
) -> RequestPasswordResetUseCase:
    return RequestPasswordResetUseCase(
        uow=uow, # type: ignore
        token_hasher=token_hasher,
        secret_generator=secrets,
        email_service=email,
    )


def get_reset_password_use_case(
    uow: IdentityUoWDep,
    hasher: PasswordHasherDep,
    token_hasher: TokenHasherDep,
) -> ResetPasswordUseCase:
    return ResetPasswordUseCase(uow=uow, password_hasher=hasher, token_hasher=token_hasher) # type: ignore


