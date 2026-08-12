from typing import Protocol
from uuid import UUID

from src.annotations.domain.entities.highlight import Highlight


class HighlightCommandRepository(Protocol):
    async def save(self, highlight: Highlight) -> None: ...

    async def delete(self, highlight_id: UUID) -> None: ...