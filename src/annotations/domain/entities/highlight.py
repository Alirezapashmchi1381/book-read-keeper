from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from src.annotations.domain.exceptions import (
    HighlightAlreadyDeletedError,
    HighlightNotDeletedError,
    SelectionRangeError,
)
from src.annotations.domain.value_objects.locator import Locator
from src.annotations.domain.value_objects.note_text import NoteText


@dataclass
class Highlight:
    id: UUID
    user_id: UUID
    locator: Locator
    end_locator: Locator
    selected_text: str
    color: str
    note: NoteText | None = None
    is_deleted: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        user_id: UUID,
        locator: Locator,
        end_locator: Locator,
        selected_text: str,
        color: str,
        note: Optional[NoteText] = None,
    ) -> "Highlight":
        if locator.book_id != end_locator.book_id:
            raise SelectionRangeError("Locator and end_locator must reference the same book")
        if not selected_text or not selected_text.strip():
            raise ValueError("selected_text cannot be empty")
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid4(),
            user_id=user_id,
            locator=locator,
            end_locator=end_locator,
            selected_text=selected_text,
            color=color,
            note=note,
            is_deleted=False,
            created_at=now,
            updated_at=now,
        )

    def edit_note(self, note: NoteText | None) -> None:
        self.note = note
        self.updated_at = datetime.now(timezone.utc)

    def change_color(self, color: str) -> None:
        self.color = color
        self.updated_at = datetime.now(timezone.utc)

    def soft_delete(self) -> None:
        if self.is_deleted:
            raise HighlightAlreadyDeletedError("Highlight is already deleted")
        self.is_deleted = True
        self.updated_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        if not self.is_deleted:
            raise HighlightNotDeletedError("Highlight is not deleted")
        self.is_deleted = False
        self.updated_at = datetime.now(timezone.utc)