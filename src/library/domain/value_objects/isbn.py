import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ISBN:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("ISBN must not be empty")
        cleaned = self.value.replace("-", "").replace(" ", "")
        if not re.match(r'^(?:\d{9}[\dXx]|\d{13})$', cleaned):
            raise ValueError(
                f"Invalid ISBN format: '{self.value}'. "
                "Expected ISBN-10 (10 digits or 9 digits + X) or ISBN-13 (13 digits)."
            )