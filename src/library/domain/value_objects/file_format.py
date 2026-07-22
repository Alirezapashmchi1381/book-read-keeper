from dataclasses import dataclass


@dataclass(frozen=True)
class FileFormat:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("File format must not be empty")