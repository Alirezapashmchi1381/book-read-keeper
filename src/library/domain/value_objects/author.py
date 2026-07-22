from dataclasses import dataclass


@dataclass(frozen=True)
class Author:
    first_name: str
    last_name: str

    def __post_init__(self) -> None:
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name must not be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name must not be empty")