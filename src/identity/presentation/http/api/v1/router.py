from fastapi import APIRouter

from src.identity.presentation.http.api.v1.endpoints.account.router import router as account_router
from src.identity.presentation.http.api.v1.endpoints.auth.router import router as auth_router
from src.identity.presentation.http.api.v1.endpoints.verification.router import router as verification_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(account_router)
v1_router.include_router(verification_router)
