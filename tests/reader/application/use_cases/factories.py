from unittest.mock import AsyncMock
from uuid import UUID, uuid4

from src.reader.domain.entities.reading_session import ReadingSession
from src.reader.domain.value_objects.device_id import DeviceId
from src.reader.domain.value_objects.locator import Locator
from src.reader.domain.value_objects.progress_percent import ProgressPercent


class FakeSubUoW:
    def __init__(self) -> None:
        self.query = AsyncMock()
        self.command = AsyncMock()


class FakeReaderUnitOfWork:
    def __init__(self) -> None:
        self.sessions = FakeSubUoW()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> "FakeReaderUnitOfWork":
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
    return Locator(
        book_id=book_id,
        value=value,
        provider=provider,
        sort_key=sort_key,
        chapter_number=chapter_number,
        chapter_title=chapter_title,
    )


def make_session(
    *,
    book_id: UUID = uuid4(),
    user_id: UUID = uuid4(),
    progress: float = 0.0,
    device_id: str | None = None,
) -> ReadingSession:
    return ReadingSession.start(
        user_id=user_id,
        book_id=book_id,
        locator=make_locator(book_id=book_id),
        progress_percent=ProgressPercent(progress),
        device_id=DeviceId(device_id) if device_id else None,
    )