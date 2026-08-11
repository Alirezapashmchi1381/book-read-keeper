from dataclasses import dataclass
import re

@dataclass(frozen=True)
class BucketID:
    _name : str

    def __post_init__(self):
            if not re.match(r"^[a-z0-9.-]{3,63}$", self._name):
                raise ValueError("Invalid bucket name format")