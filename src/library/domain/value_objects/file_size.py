from dataclasses import dataclass


@dataclass(frozen=True)
class FileSize:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError(f"File size must be positive, got {self.value}")