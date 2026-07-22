import re
from dataclasses import dataclass


@dataclass(frozen=True)
class StorageKey:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Storage key cannot be empty")
        if not re.match(r'^[a-zA-Z0-9_./-]+$', self.value):
            raise ValueError(
                f"Invalid storage key: '{self.value}'. "
                "Only alphanumeric characters, underscores, dots, "
                "slashes, and hyphens are allowed."
            )