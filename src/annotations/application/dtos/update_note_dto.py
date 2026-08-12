from dataclasses import dataclass
from uuid import UUID

from src.annotations.domain.value_objects.note_text import NoteText


@dataclass(frozen=True)
class UpdateNoteInputDto:
    highlight_id: UUID
    note: str | None

    def to_note(self) -> NoteText | None:
        if self.note is None:
            return None
        return NoteText(self.note)