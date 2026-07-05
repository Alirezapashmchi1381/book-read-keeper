import hashlib
import hmac as _hmac


class HMACTokenHasher:
    def __init__(self, secret: str) -> None:
        self._secret = secret.encode("utf-8")

    def hash(self, token: str) -> str:
        return _hmac.digest(self._secret, token.encode("utf-8"), hashlib.sha256).hex()

    def verify(self, token: str, hashed: str) -> bool:
        return _hmac.compare_digest(self.hash(token), hashed)
