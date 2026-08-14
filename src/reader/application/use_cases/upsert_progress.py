from dataclasses import dataclass

from src.reader.application.dtos.session_output_dto import SessionOutputDto
from src.reader.application.dtos.upsert_progress_dto import UpsertProgressInputDto
from src.reader.domain.entities.reading_session import ReadingSession
from src.reader.domain.exceptions import ReadingSessionNotFoundError
from src.reader.domain.ports.unit_of_work import ReaderUnitOfWork


@dataclass
class UpsertProgressUseCase:
    """Updates position on existing session (LWW by updated_at)."""
    uow: ReaderUnitOfWork

    async def execute(self, dto: UpsertProgressInputDto) -> SessionOutputDto:
        async with self.uow as uow:
            session = await uow.sessions.query.find_by_user_and_book(dto.user_id, dto.book_id)
            if session is None:
                raise ReadingSessionNotFoundError(
                    f"No reading session for user {dto.user_id}, book {dto.book_id}"
                )

            session.update_position(
                locator=dto.to_locator(),
                progress_percent=dto.to_progress(),
                device_id=dto.to_device_id(),
            )
            await uow.sessions.command.save(session)
            await uow.commit()
            return self._to_output(session)

    def _to_output(self, session: ReadingSession) -> SessionOutputDto:
        return SessionOutputDto(
            id=session.id,
            user_id=session.user_id,
            book_id=session.book_id,
            locator_value=session.locator.value,
            locator_provider=session.locator.provider,
            locator_sort_key=session.locator.sort_key,
            locator_chapter_number=session.locator.chapter_number,
            locator_chapter_title=session.locator.chapter_title,
            progress_percent=session.progress_percent.value,
            device_id=session.device_id.value if session.device_id else None,
            started_at=session.started_at,
            updated_at=session.updated_at,
        )