import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


class RS256TokenService:
    def __init__(
        self,
        private_key: RSAPrivateKey,
        public_key: RSAPublicKey,
        issuer: str,
        access_token_ttl_minutes: int = 15,
    ) -> None:
        self._private_key = private_key
        self._public_key = public_key
        self._issuer = issuer
        self._access_token_ttl = timedelta(minutes=access_token_ttl_minutes)

    def generate_access_token(self, user_id: UUID) -> str:
        now = datetime.now(tz=timezone.utc)
        payload = {
            "sub": str(user_id),
            "iss": self._issuer,
            "iat": now,
            "exp": now + self._access_token_ttl,
        }
        return jwt.encode(payload, self._private_key, algorithm="RS256")

    def generate_refresh_token(self) -> str:
        return secrets.token_urlsafe(32)

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self._public_key,
            algorithms=["RS256"],
            issuer=self._issuer,
        )
