from uuid import uuid4

import pytest

from src.reader.infrastructure.sql.repository.sqlalchemy_reading_session_command_repository import (
    SQLAlchemyReadingSessionCommandRepository,
)
from src.reader.infrastructure.sql.repository.sqlalchemy_reading_session_query_repository import (
    SQLAlchemyReadingSessionQueryRepository,
)

from tests.reader.infrastructure.factories import make_session


@pytest.mark.asyncio
class TestReadingSessionCommandRepository:
    async def test_save_and_find_by_id(self, session) -> None:
        command = SQLAlchemyReadingSessionCommandRepository(session)
        sess = make_session(progress=10.0, device_id="device-1")
        await command.save(sess)
        await session.commit()

        query = SQLAlchemyReadingSessionQueryRepository(session)
        found = await query.find_by_id(sess.id)

        assert found is not None
        assert found.id == sess.id
        assert found.progress_percent.value == 10.0
        assert found.device_id is not None
        assert found.device_id.value == "device-1"

    async def test_delete(self, session) -> None:
        command = SQLAlchemyReadingSessionCommandRepository(session)
        sess = make_session()
        await command.save(sess)
        await session.commit()

        await command.delete(sess.id)
        await session.commit()

        query = SQLAlchemyReadingSessionQueryRepository(session)
        found = await query.find_by_id(sess.id)
        assert found is None


@pytest.mark.asyncio
class TestReadingSessionQueryRepository:
    async def test_find_by_user_and_book(self, session) -> None:
        command = SQLAlchemyReadingSessionCommandRepository(session)
        sess = make_session(progress=25.0)
        await command.save(sess)
        await session.commit()

        query = SQLAlchemyReadingSessionQueryRepository(session)
        found = await query.find_by_user_and_book(sess.user_id, sess.book_id)

        assert found is not None
        assert found.id == sess.id
        assert found.progress_percent.value == 25.0

    async def test_find_by_user_and_book_returns_none(self, session) -> None:
        query = SQLAlchemyReadingSessionQueryRepository(session)
        found = await query.find_by_user_and_book(uuid4(), uuid4())
        assert found is None

    async def test_list_by_user(self, session) -> None:
        command = SQLAlchemyReadingSessionCommandRepository(session)
        user_id = uuid4()
        s1 = make_session(user_id=user_id, progress=10.0)
        s2 = make_session(user_id=user_id, progress=50.0)
        other = make_session()
        await command.save(s1)
        await command.save(s2)
        await command.save(other)
        await session.commit()

        query = SQLAlchemyReadingSessionQueryRepository(session)
        results = await query.list_by_user(user_id)

        assert len(results) == 2
        assert {r.id for r in results} == {s1.id, s2.id}