from dataclasses import dataclass
from uuid import UUID

from src.annotations.domain.value_objects.chapter import Chapter
from src.annotations.domain.value_objects.locator import Locator
from src.annotations.domain.value_objects.note_text import NoteText


@dataclass(frozen=True)
class CreateHighlightInputDto:
    user_id: UUID
    book_id: UUID
    selected_text: str
    color: str
    # start locator (required)
    start_value: str
    start_provider: str
    start_sort_key: str
    # end locator (required)
    end_value: str
    end_provider: str
    end_sort_key: str
    # start locator (optional)
    start_chapter_number: int | None = None
    start_chapter_title: str | None = None
    # end locator (optional)
    end_chapter_number: int | None = None
    end_chapter_title: str | None = None
    # note (optional)
    note: str | None = None

    def _chapter(self, number: int | None, title: str | None) -> Chapter | None:
        if number is None:
            return None
        return Chapter(number=number, title=title)

    def to_start_locator(self) -> Locator:
        return Locator(
            book_id=self.book_id,
            chapter=self._chapter(self.start_chapter_number, self.start_chapter_title),
            value=self.start_value,
            provider=self.start_provider,
            sort_key=self.start_sort_key,
        )

    def to_end_locator(self) -> Locator:
        return Locator(
            book_id=self.book_id,
            chapter=self._chapter(self.end_chapter_number, self.end_chapter_title),
            value=self.end_value,
            provider=self.end_provider,
            sort_key=self.end_sort_key,
        )

    def to_note(self) -> NoteText | None:
        if self.note is None:
            return None
        return NoteText(self.note)