import pytest

from src.storage.domain.value_objects.object_key import ObjectKey

from tests.storage.infrastructure.factories import make_object


@pytest.mark.asyncio
class TestStorageUnitOfWork:
    async def test_commit_saves_object(self, storage_uow) -> None:
        async with storage_uow as uow:
            await uow.objects.command.save(make_object(key="books/1/file.epub"))

        # After commit, the object should be queryable in a new session.
        async with storage_uow as uow2:
            found = await uow2.objects.query.find_by_key(ObjectKey("books/1/file.epub"))
            assert found is not None
            assert found.key._value == "books/1/file.epub"

    async def test_rollback_on_exception(self, storage_uow) -> None:
        with pytest.raises(RuntimeError):
            async with storage_uow as uow:
                await uow.objects.command.save(make_object(key="books/1/file.epub"))
                raise RuntimeError("boom")

        # The object should not be persisted after rollback.
        async with storage_uow as uow2:
            found = await uow2.objects.query.find_by_key(ObjectKey("books/1/file.epub"))
            assert found is None

    async def test_delete_via_command(self, storage_uow) -> None:
        async with storage_uow as uow:
            await uow.objects.command.save(make_object(key="books/1/file.epub"))

        async with storage_uow as uow:
            await uow.objects.command.delete(ObjectKey("books/1/file.epub"))

        async with storage_uow as uow:
            found = await uow.objects.query.find_by_key(ObjectKey("books/1/file.epub"))
            assert found is None