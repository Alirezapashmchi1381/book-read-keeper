import pytest

from tests.annotations.infrastructure.factories import make_highlight


@pytest.mark.asyncio
class TestAnnotationsUnitOfWork:
    async def test_commit_saves_highlight(self, annotations_uow) -> None:
        highlight = make_highlight(selected_text="persisted")
        async with annotations_uow as uow:
            await uow.highlights.command.save(highlight)

        # A new uow/session sees the committed row.
        async with annotations_uow as uow:
            found = await uow.highlights.query.find_by_id(highlight.id)
            assert found is not None
            assert found.selected_text == "persisted"

    async def test_rollback_on_exception(self, annotations_uow) -> None:
        highlight = make_highlight(selected_text="rollback")
        with pytest.raises(RuntimeError):
            async with annotations_uow as uow:
                await uow.highlights.command.save(highlight)
                raise RuntimeError("boom")

        # The row should not exist after rollback.
        async with annotations_uow as uow:
            found = await uow.highlights.query.find_by_id(highlight.id)
            assert found is None

    async def test_delete_via_command(self, annotations_uow) -> None:
        highlight = make_highlight(selected_text="to delete")
        async with annotations_uow as uow:
            await uow.highlights.command.save(highlight)

        async with annotations_uow as uow:
            await uow.highlights.command.delete(highlight)

        async with annotations_uow as uow:
            found = await uow.highlights.query.find_by_id(highlight.id)
            assert found is None