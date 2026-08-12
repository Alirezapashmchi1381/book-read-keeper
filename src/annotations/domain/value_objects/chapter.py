from dataclasses import dataclass


@dataclass(frozen=True)
class Chapter:
    number: int
    title: str | None = None

    def __post_init__(self) -> None:
        if self.number <= 0:
            raise ValueError(f"Chapter number must be positive, got {self.number}")
        if self.title is not None and not self.title.strip():
            raise ValueError("Chapter title cannot be empty")