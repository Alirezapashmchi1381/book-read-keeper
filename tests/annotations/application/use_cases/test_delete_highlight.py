from uuid import uuid4

import pytest

from src.annotations.application.use_cases.delete_highlight import DeleteHighlightUseCase
from src.annotations.domain.exceptions import HighlightNotFoundError

from tests.annotations.application.use_cases.factories import make_highlight


class TestDeleteHighlightUseCase:
    async def test_soft_deletes_highlight(self, fake_uow) -> None:
        highlight = make_highlight()
        fake_uow.highlights.query.find_by_id.return_value = highlight

        use_case = DeleteHighlightUseCase(uow=fake_uow)
        await use_case.execute(highlight.id)

        fake_uow.highlights.query.find_by_id.assert_awaited_once_with(highlight.id)
        assert highlight.is_deleted is True
        fake_uow.highlights.command.delete.assert_awaited_once_with(highlight)
        assert fake_uow.committed is True

    async def test_raises_when_highlight_not_found(self, fake_uow) -> None:
        fake_uow.highlights.query.find_by_id.return_value = None

        use_case = DeleteHighlightUseCase(uow=fake_uow)
        with pytest.raises(HighlightNotFoundError):
            await use_case.execute(uuid4())

        fake_uow.highlights.command.delete.assert_not_awaited()