from typing import Protocol


class SecretGenerator(Protocol):
    def generate(self) -> str: ...
