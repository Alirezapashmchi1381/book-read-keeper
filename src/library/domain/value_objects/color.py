import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    hex_value: str

    def __post_init__(self) -> None:
        if not re.match(r'^#[0-9a-fA-F]{6}$', self.hex_value):
            raise ValueError(
                f"Invalid color: '{self.hex_value}'. "
                "Expected a hex color code like '#FF5733'."
            )