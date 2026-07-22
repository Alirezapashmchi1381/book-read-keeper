from dataclasses import dataclass


@dataclass(frozen=True)
class Checksum:
    algorithm: str
    value: str

    def __post_init__(self) -> None:
        if not self.algorithm or not self.value:
            raise ValueError("Algorithm and value must not be empty")