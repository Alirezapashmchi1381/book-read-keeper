from uuid import uuid4

import pytest

from src.annotations.application.dtos.update_note_dto import UpdateNoteInputDto
from src.annotations.application.use_cases.update_note import UpdateNoteUseCase
from src.annotations.domain.exceptions import HighlightNotFoundError

from tests.annotations.application.use_cases.factories import make_highlight


class TestUpdateNoteUseCase:
    async def test_updates_note(self, fake_uow) -> None:
        highlight = make_highlight()
        fake_uow.highlights.query.find_by_id.return_value = highlight

        use_case = UpdateNoteUseCase(uow=fake_uow)
        result = await use_case.execute(UpdateNoteInputDto(highlight_id=highlight.id, note="updated note"))

        assert result.note is not None
        assert result.note.value == "updated note"
        fake_uow.highlights.command.save.assert_awaited_once_with(highlight)
        assert fake_uow.committed is True

    async def test_clear_note(self, fake_uow) -> None:
        highlight = make_highlight(note="old note")
        fake_uow.highlights.query.find_by_id.return_value = highlight

        use_case = UpdateNoteUseCase(uow=fake_uow)
        result = await use_case.execute(UpdateNoteInputDto(highlight_id=highlight.id, note=None))

        assert result.note is None
        fake_uow.highlights.command.save.assert_awaited_once_with(highlight)

    async def test_raises_when_highlight_not_found(self, fake_uow) -> None:
        fake_uow.highlights.query.find_by_id.return_value = None

        use_case = UpdateNoteUseCase(uow=fake_uow)
        with pytest.raises(HighlightNotFoundError):
            await use_case.execute(UpdateNoteInputDto(highlight_id=uuid4(), note="note"))

        fake_uow.highlights.command.save.assert_not_awaited()