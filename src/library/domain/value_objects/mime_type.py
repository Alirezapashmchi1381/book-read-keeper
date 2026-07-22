import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MimeType:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("MIME type must not be empty")
        # Validate format: type/subtype
        if not re.match(r'^[a-zA-Z0-9.+-]+/[a-zA-Z0-9.+-]+$', self.value.strip()):
            raise ValueError(
                f"Invalid MIME type format: '{self.value}'. "
                "Expected format: 'type/subtype' (e.g. 'application/pdf')."
            )