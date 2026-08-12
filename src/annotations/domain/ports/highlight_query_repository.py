from typing import Protocol
from uuid import UUID

from src.annotations.domain.entities.highlight import Highlight


class HighlightQueryRepository(Protocol):
    async def find_by_id(self, highlight_id: UUID) -> Highlight | None: ...

    async def find_by_book(
        self,
        user_id: UUID,
        book_id: UUID,
        chapter: int | None = None,
    ) -> list[Highlight]: ...

    async def list_by_user(self, user_id: UUID) -> list[Highlight]: ...