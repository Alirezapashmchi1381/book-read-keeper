from typing import Protocol
from uuid import UUID

from src.reader.domain.entities.reading_session import ReadingSession


class ReadingSessionCommandRepository(Protocol):
    async def save(self, session: ReadingSession) -> None: ...

    async def delete(self, session_id: UUID) -> None: ...