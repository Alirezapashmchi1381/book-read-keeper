from dataclasses import dataclass

from src.annotations.application.dtos.create_highlight_dto import CreateHighlightInputDto
from src.annotations.domain.entities.highlight import Highlight
from src.annotations.domain.ports.unit_of_work import AnnotationsUnitOfWork


@dataclass
class CreateHighlightUseCase:
    uow: AnnotationsUnitOfWork

    async def execute(self, dto: CreateHighlightInputDto) -> Highlight:
        async with self.uow as uow:
            highlight = Highlight.create(
                user_id=dto.user_id,
                locator=dto.to_start_locator(),
                end_locator=dto.to_end_locator(),
                selected_text=dto.selected_text,
                color=dto.color,
                note=dto.to_note(),
            )
            await uow.highlights.command.save(highlight)
            await uow.commit()
            return highlight