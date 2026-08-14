import pytest

from tests.reader.infrastructure.factories import make_session


@pytest.mark.asyncio
class TestReaderUnitOfWork:
    async def test_commit_saves_session(self, reader_uow) -> None:
        sess = make_session(progress=10.0)
        async with reader_uow as uow:
            await uow.sessions.command.save(sess)

        async with reader_uow as uow2:
            found = await uow2.sessions.query.find_by_id(sess.id)
            assert found is not None
            assert found.progress_percent.value == 10.0

    async def test_rollback_on_exception(self, reader_uow) -> None:
        sess = make_session()
        with pytest.raises(RuntimeError):
            async with reader_uow as uow:
                await uow.sessions.command.save(sess)
                raise RuntimeError("boom")

        async with reader_uow as uow:
            found = await uow.sessions.query.find_by_id(sess.id)
            assert found is None

    async def test_find_by_user_and_book_via_uow(self, reader_uow) -> None:
        sess = make_session(progress=50.0)
        async with reader_uow as uow:
            await uow.sessions.command.save(sess)

        async with reader_uow as uow:
            found = await uow.sessions.query.find_by_user_and_book(sess.user_id, sess.book_id)
            assert found is not None
            assert found.id == sess.id
            assert found.progress_percent.value == 50.0