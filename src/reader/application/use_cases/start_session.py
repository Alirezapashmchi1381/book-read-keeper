from dataclasses import dataclass

from src.reader.application.dtos.session_output_dto import SessionOutputDto
from src.reader.application.dtos.start_session_dto import StartSessionInputDto
from src.reader.domain.entities.reading_session import ReadingSession
from src.reader.domain.ports.unit_of_work import ReaderUnitOfWork


@dataclass
class StartSessionUseCase:
    """Idempotent: finds existing session for (user, book) or creates a new one."""
    uow: ReaderUnitOfWork

    async def execute(self, dto: StartSessionInputDto) -> SessionOutputDto:
        async with self.uow as uow:
            existing = await uow.sessions.query.find_by_user_and_book(dto.user_id, dto.book_id)
            if existing is not None:
                return self._to_output(existing)

            session = ReadingSession.start(
                user_id=dto.user_id,
                book_id=dto.book_id,
                locator=dto.to_locator(),
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