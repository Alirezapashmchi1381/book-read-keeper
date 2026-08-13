from uuid import UUID, uuid4

from src.annotations.domain.entities.highlight import Highlight
from src.annotations.domain.value_objects.chapter import Chapter
from src.annotations.domain.value_objects.locator import Locator
from src.annotations.domain.value_objects.note_text import NoteText


def make_locator(
    *,
    book_id: UUID = uuid4(),
    value: str = "epubcfi(/6/4!/4/2)",
    provider: str = "epub",
    sort_key: str = "1.0",
    chapter_number: int | None = 1,
    chapter_title: str | None = "Chapter 1",
) -> Locator:
    chapter = None
    if chapter_number is not None:
        chapter = Chapter(number=chapter_number, title=chapter_title)
    return Locator(
        book_id=book_id,
        value=value,
        provider=provider,
        sort_key=sort_key,
        chapter=chapter,
    )


def make_highlight(
    *,
    book_id: UUID = uuid4(),
    user_id: UUID = uuid4(),
    selected_text: str = "some highlighted text",
    color: str = "#FF5733",
    note: str | None = None,
    is_deleted: bool = False,
    chapter_number: int | None = 1,
    chapter_title: str | None = "Chapter 1",
) -> Highlight:
    highlight = Highlight(
        id=uuid4(),
        user_id=user_id,
        locator=make_locator(book_id=book_id, chapter_number=chapter_number, chapter_title=chapter_title),
        end_locator=make_locator(book_id=book_id, sort_key="1.1", chapter_number=chapter_number, chapter_title=chapter_title),
        selected_text=selected_text,
        color=color,
        note=NoteText(note) if note else None,
        is_deleted=is_deleted,
    )
    return highlight
