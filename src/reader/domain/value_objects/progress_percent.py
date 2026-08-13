from dataclasses import dataclass

from src.reader.domain.exceptions import InvalidProgressError


@dataclass(frozen=True)
class ProgressPercent:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0.0 or self.value > 100.0:
            raise InvalidProgressError(f"Progress must be 0.0–100.0, got {self.value}")