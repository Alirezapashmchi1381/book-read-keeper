from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.config import Settings, get_settings
from src.identity.infrastructure.services.jwt_token_service import JWTTokenService

_bearer = HTTPBearer()


def _get_jwt_token_service(settings: Settings = Depends(get_settings)) -> JWTTokenService:
    return JWTTokenService(
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.jwt_access_token_expire_minutes,
    )


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    token_service: JWTTokenService = Depends(_get_jwt_token_service),
) -> UUID:
    """FastAPI dependency that extracts the authenticated user ID from the JWT access token.

    Expects an ``Authorization: Bearer <token>`` header.
    Raises HTTPException(401) if the token is missing, invalid, or expired.
    """
    try:
        return token_service.verify_access_token(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )