from dataclasses import dataclass


@dataclass(frozen=True)
class ShelfName:
    name: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Shelf name cannot be empty")