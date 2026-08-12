from unittest.mock import AsyncMock
from uuid import UUID, uuid4

from src.annotations.domain.entities.highlight import Highlight
from src.annotations.domain.value_objects.chapter import Chapter
from src.annotations.domain.value_objects.locator import Locator
from src.annotations.domain.value_objects.note_text import NoteText


class FakeSubUoW:
    def __init__(self) -> None:
        self.query = AsyncMock()
        self.command = AsyncMock()


class FakeAnnotationsUnitOfWork:
    def __init__(self) -> None:
        self.highlights = FakeSubUoW()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> "FakeAnnotationsUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.committed = True
        else:
            self.rolled_back = True

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True


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
) -> Highlight:
    highlight = Highlight.create(
        user_id=user_id,
        locator=make_locator(book_id=book_id),
        end_locator=make_locator(book_id=book_id, sort_key="1.1"),
        selected_text=selected_text,
        color=color,
        note=NoteText(note) if note else None,
    )
    if is_deleted:
        highlight.soft_delete()
    return highlight