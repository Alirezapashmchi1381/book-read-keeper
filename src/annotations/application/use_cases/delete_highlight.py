from dataclasses import dataclass
from uuid import UUID

from src.annotations.domain.exceptions import HighlightNotFoundError
from src.annotations.domain.ports.unit_of_work import AnnotationsUnitOfWork


@dataclass
class DeleteHighlightUseCase:
    uow: AnnotationsUnitOfWork

    async def execute(self, highlight_id: UUID) -> None:
        async with self.uow as uow:
            highlight = await uow.highlights.query.find_by_id(highlight_id)
            if highlight is None:
                raise HighlightNotFoundError(f"Highlight {highlight_id} not found")
            highlight.soft_delete()
            await uow.highlights.command.delete(highlight)
            await uow.commit()
