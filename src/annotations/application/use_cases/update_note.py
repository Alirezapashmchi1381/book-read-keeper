from dataclasses import dataclass

from src.annotations.application.dtos.update_note_dto import UpdateNoteInputDto
from src.annotations.domain.entities.highlight import Highlight
from src.annotations.domain.exceptions import HighlightNotFoundError
from src.annotations.domain.ports.unit_of_work import AnnotationsUnitOfWork


@dataclass
class UpdateNoteUseCase:
    uow: AnnotationsUnitOfWork

    async def execute(self, dto: UpdateNoteInputDto) -> Highlight:
        async with self.uow as uow:
            highlight = await uow.highlights.query.find_by_id(dto.highlight_id)
            if highlight is None:
                raise HighlightNotFoundError(f"Highlight {dto.highlight_id} not found")
            highlight.edit_note(dto.to_note())
            await uow.highlights.command.save(highlight)
            await uow.commit()
            return highlight