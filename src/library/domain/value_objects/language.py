import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    code: str

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValueError("Language code must not be empty")
        # Allow ISO 639‑1 (2 letters) or ISO 639‑2 (3 letters)
        if not re.match(r'^[a-zA-Z]{2,3}$', self.code.strip()):
            raise ValueError(
                f"Invalid language code: '{self.code}'. "
                "Expected a 2 or 3 letter ISO language code."
            )