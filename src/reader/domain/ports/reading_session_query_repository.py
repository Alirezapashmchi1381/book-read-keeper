from typing import Protocol
from uuid import UUID

from src.reader.domain.entities.reading_session import ReadingSession


class ReadingSessionQueryRepository(Protocol):
    async def find_by_id(self, session_id: UUID) -> ReadingSession | None: ...

    async def find_by_user_and_book(self, user_id: UUID, book_id: UUID) -> ReadingSession | None: ...

    async def list_by_user(self, user_id: UUID) -> list[ReadingSession]: ...