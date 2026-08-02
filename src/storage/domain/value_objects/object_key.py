from dataclasses import dataclass
import re

@dataclass(frozen=True)
class ObjectKey:
    _value : str

    def __post_init__(self):
        if not self._value or len(self._value) > 1024:
            raise ValueError("Key must be 1-1024 characters")
        if self._value.startswith("/") or self._value.endswith("/"):
            raise ValueError("Key cannot start or end with '/'")