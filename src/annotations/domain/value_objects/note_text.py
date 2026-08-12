from dataclasses import dataclass


@dataclass(frozen=True)
class NoteText:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("Note text cannot be empty")