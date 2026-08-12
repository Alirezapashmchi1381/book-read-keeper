from dataclasses import dataclass
from uuid import UUID

from src.annotations.application.dtos.highlight_output_dto import (
    HighlightOutputDto,
    LocatorOutputDto,
)
from src.annotations.domain.entities.highlight import Highlight
from src.annotations.domain.ports.unit_of_work import AnnotationsUnitOfWork


@dataclass
class ListHighlightsUseCase:
    uow: AnnotationsUnitOfWork

    async def execute(self, user_id: UUID, book_id: UUID, chapter: int | None = None) -> list[HighlightOutputDto]:
        async with self.uow as uow:
            highlights = await uow.highlights.query.find_by_book(user_id, book_id, chapter)
            return [self._to_output(h) for h in highlights]

    def _to_output(self, highlight: Highlight) -> HighlightOutputDto:
        return HighlightOutputDto(
            id=highlight.id,
            selected_text=highlight.selected_text,
            color=highlight.color,
            note=highlight.note.value if highlight.note else None,
            locator=self._to_locator(highlight.locator),
            end_locator=self._to_locator(highlight.end_locator),
            is_deleted=highlight.is_deleted,
            created_at=highlight.created_at,
            updated_at=highlight.updated_at,
        )

    def _to_locator(self, locator) -> LocatorOutputDto:
        return LocatorOutputDto(
            book_id=locator.book_id,
            chapter_number=locator.chapter.number if locator.chapter else None,
            chapter_title=locator.chapter.title if locator.chapter else None,
            value=locator.value,
            provider=locator.provider,
            sort_key=locator.sort_key,
        )