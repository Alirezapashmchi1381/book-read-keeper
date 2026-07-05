from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt


class JWTTokenService:
    def __init__(self, secret: str, algorithm: str = "HS256", expire_minutes: int = 30) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def generate_access_token(self, user_id: UUID) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def verify_access_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return UUID(payload["sub"])
        except Exception as exc:
            raise ValueError("Invalid or expired access token") from exc
