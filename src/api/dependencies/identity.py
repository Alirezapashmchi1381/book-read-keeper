from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.identity.application.use_cases.login import LoginUseCase
from src.identity.application.use_cases.signup import SignupUseCase
from src.identity.repository.unit_of_work import SQLAlchemyIdentityUnitOfWork

# ------------------------------------------------------------------
# Infrastructure singletons -- created once at import time.
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

# from src.identity.infrastructure.password_hasher import ArgonPasswordHasher
# from src.identity.infrastructure.token_service import JWTTokenService
# _password_hasher = ArgonPasswordHasher()
# _token_service = JWTTokenService(secret=settings.jwt_secret)

# ------------------------------------------------------------------
# Per-request dependencies
# ------------------------------------------------------------------

def get_uow() -> SQLAlchemyIdentityUnitOfWork:
    """
    Creates a new UoW for each request.
    Cheap: it only holds a reference to the session factory.
    The actual DB session is opened inside use_case.execute().
    """
    return SQLAlchemyIdentityUnitOfWork(_session_factory)


UoWDep = Annotated[SQLAlchemyIdentityUnitOfWork, Depends(get_uow)]


def get_signup_use_case(uow: UoWDep) -> SignupUseCase:
    return SignupUseCase(
        uow=uow,
        password_hasher=...,  # replace: ArgonPasswordHasher()
        token_service=...,    # replace: JWTTokenService(...)
    )


def get_login_use_case(uow: UoWDep) -> LoginUseCase:
    return LoginUseCase(
        uow=uow,
        password_hasher=...,  # replace: ArgonPasswordHasher()
        token_service=...,    # replace: JWTTokenService(...)
    )


SignupUseCaseDep = Annotated[SignupUseCase, Depends(get_signup_use_case)]
LoginUseCaseDep = Annotated[LoginUseCase, Depends(get_login_use_case)]
