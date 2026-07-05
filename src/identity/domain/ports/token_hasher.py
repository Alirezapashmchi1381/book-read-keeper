from typing import Protocol


class TokenHasher(Protocol):
    def hash(self, token: str) -> str: ...

    def verify(self, token: str, hashed: str) -> bool: ...
