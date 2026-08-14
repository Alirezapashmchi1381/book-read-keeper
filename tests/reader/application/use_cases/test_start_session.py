from uuid import uuid4

from src.reader.application.dtos.start_session_dto import StartSessionInputDto
from src.reader.application.use_cases.start_session import StartSessionUseCase

from tests.reader.application.use_cases.factories import make_session


class TestStartSessionUseCase:
    async def test_creates_new_session(self, fake_uow) -> None:
        user_id = uuid4()
        book_id = uuid4()
        fake_uow.sessions.query.find_by_user_and_book.return_value = None

        use_case = StartSessionUseCase(uow=fake_uow)
        result = await use_case.execute(
            StartSessionInputDto(
                user_id=user_id,
                book_id=book_id,
                locator_value="cfi-1",
                locator_provider="epub",
                locator_sort_key="1.0",
                locator_chapter_number=1,
                locator_chapter_title="Chapter 1",
                device_id="device-1",
            )
        )

        assert result.user_id == user_id
        assert result.book_id == book_id
        assert result.progress_percent == 0.0
        assert result.device_id == "device-1"
        fake_uow.sessions.command.save.assert_awaited_once()
        assert fake_uow.committed is True

    async def test_returns_existing_session_idempotent(self, fake_uow) -> None:
        session = make_session()
        fake_uow.sessions.query.find_by_user_and_book.return_value = session

        use_case = StartSessionUseCase(uow=fake_uow)
        result = await use_case.execute(
            StartSessionInputDto(
                user_id=session.user_id,
                book_id=session.book_id,
                locator_value="cfi-1",
                locator_provider="epub",
                locator_sort_key="1.0",
            )
        )

        assert result.id == session.id
        fake_uow.sessions.command.save.assert_not_awaited()