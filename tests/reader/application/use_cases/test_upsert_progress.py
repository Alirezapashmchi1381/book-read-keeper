import pytest

from src.reader.application.dtos.upsert_progress_dto import UpsertProgressInputDto
from src.reader.application.use_cases.upsert_progress import UpsertProgressUseCase
from src.reader.domain.exceptions import ReadingSessionNotFoundError

from tests.reader.application.use_cases.factories import make_session


class TestUpsertProgressUseCase:
    async def test_updates_position(self, fake_uow) -> None:
        session = make_session(progress=0.0)
        fake_uow.sessions.query.find_by_user_and_book.return_value = session

        use_case = UpsertProgressUseCase(uow=fake_uow)
        result = await use_case.execute(
            UpsertProgressInputDto(
                user_id=session.user_id,
                book_id=session.book_id,
                locator_value="cfi-2",
                locator_provider="epub",
                locator_sort_key="2.0",
                progress_percent=50.0,
                device_id="device-2",
            )
        )

        assert result.locator_value == "cfi-2"
        assert result.progress_percent == 50.0
        assert result.device_id == "device-2"
        fake_uow.sessions.command.save.assert_awaited_once_with(session)
        assert fake_uow.committed is True

    async def test_raises_when_session_not_found(self, fake_uow) -> None:
        fake_uow.sessions.query.find_by_user_and_book.return_value = None

        use_case = UpsertProgressUseCase(uow=fake_uow)
        with pytest.raises(ReadingSessionNotFoundError):
            await use_case.execute(
                UpsertProgressInputDto(
                    user_id=__import__("uuid").uuid4(),
                    book_id=__import__("uuid").uuid4(),
                    locator_value="cfi-1",
                    locator_provider="epub",
                    locator_sort_key="1.0",
                )
            )

        fake_uow.sessions.command.save.assert_not_awaited()