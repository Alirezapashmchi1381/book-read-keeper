import pytest

from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.infrastructure.sql.repository.sqlalchemy_object_command_repository import (
    SQLAlchemyObjectCommandRepository,
)
from src.storage.infrastructure.sql.repository.sqlalchemy_object_query_repository import (
    SQLAlchemyObjectQueryRepository,
)

from tests.storage.infrastructure.factories import make_object


@pytest.mark.asyncio
class TestObjectCommandRepository:
    async def test_save_and_find_by_key(self, session) -> None:
        repo = SQLAlchemyObjectCommandRepository(session)
        obj = make_object(key="books/1/file.epub", etag="abc123")

        await repo.save(obj)
        await session.commit()

        query_repo = SQLAlchemyObjectQueryRepository(session)
        found = await query_repo.find_by_key(ObjectKey("books/1/file.epub"))

        assert found is not None
        assert found.key._value == "books/1/file.epub"
        assert found.etag._name == "abc123"

    async def test_delete(self, session) -> None:
        command = SQLAlchemyObjectCommandRepository(session)
        obj = make_object(key="books/1/file.epub")
        await command.save(obj)
        await session.commit()

        await command.delete(ObjectKey("books/1/file.epub"))
        await session.commit()

        query_repo = SQLAlchemyObjectQueryRepository(session)
        found = await query_repo.find_by_key(ObjectKey("books/1/file.epub"))
        assert found is None


@pytest.mark.asyncio
class TestObjectQueryRepository:
    async def test_list_all(self, session) -> None:
        command = SQLAlchemyObjectCommandRepository(session)
        await command.save(make_object(key="books/1/file.epub"))
        await command.save(make_object(key="books/2/file.pdf"))
        await session.commit()

        query_repo = SQLAlchemyObjectQueryRepository(session)
        objects = await query_repo.list_all()

        assert len(objects) == 2
        assert {o.key._value for o in objects} == {
            "books/1/file.epub",
            "books/2/file.pdf",
        }

    async def test_search_by_prefix(self, session) -> None:
        command = SQLAlchemyObjectCommandRepository(session)
        await command.save(make_object(key="books/1/file.epub"))
        await command.save(make_object(key="covers/1/cover.jpg"))
        await session.commit()

        query_repo = SQLAlchemyObjectQueryRepository(session)
        objects = await query_repo.search_by_prefix("books/")

        assert len(objects) == 1
        assert objects[0].key._value == "books/1/file.epub"

    async def test_find_by_key_returns_none_when_missing(self, session) -> None:
        query_repo = SQLAlchemyObjectQueryRepository(session)
        found = await query_repo.find_by_key(ObjectKey("missing/key"))
        assert found is None