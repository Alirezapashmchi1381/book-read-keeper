from dataclasses import dataclass

from src.library.domain.value_objects.storage_key import StorageKey


@dataclass(frozen=True)
class Cover:
    storage_key: StorageKey
    width: int
    height: int
    generated: bool

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError(f"Width must be positive, got {self.width}")
        if self.height <= 0:
            raise ValueError(f"Height must be positive, got {self.height}")
