import pytest
from uuid import uuid4

from src.reader.application.use_cases.get_progress import GetProgressUseCase
from src.reader.domain.exceptions import ReadingSessionNotFoundError

from tests.reader.application.use_cases.factories import make_session


class TestGetProgressUseCase:
    async def test_returns_session(self, fake_uow) -> None:
        session = make_session(progress=42.5)
        fake_uow.sessions.query.find_by_user_and_book.return_value = session

        use_case = GetProgressUseCase(uow=fake_uow)
        result = await use_case.execute(session.user_id, session.book_id)

        assert result.id == session.id
        assert result.progress_percent == 42.5
        assert result.locator_value == session.locator.value

    async def test_raises_when_not_found(self, fake_uow) -> None:
        fake_uow.sessions.query.find_by_user_and_book.return_value = None

        use_case = GetProgressUseCase(uow=fake_uow)
        with pytest.raises(ReadingSessionNotFoundError):
            await use_case.execute(uuid4(), uuid4())