from uuid import uuid4

from src.annotations.application.use_cases.list_highlights import ListHighlightsUseCase

from tests.annotations.application.use_cases.factories import make_highlight


class TestListHighlightsUseCase:
    async def test_lists_highlights_for_book(self, fake_uow) -> None:
        user_id = uuid4()
        book_id = uuid4()
        highlight = make_highlight(book_id=book_id, user_id=user_id, note="note")
        fake_uow.highlights.query.find_by_book.return_value = [highlight]

        use_case = ListHighlightsUseCase(uow=fake_uow)
        result = await use_case.execute(user_id, book_id)

        fake_uow.highlights.query.find_by_book.assert_awaited_once_with(user_id, book_id, None)
        assert len(result) == 1
        output = result[0]
        assert output.id == highlight.id
        assert output.selected_text == highlight.selected_text
        assert output.note == "note"
        assert output.locator.chapter_number == 1
        assert output.locator.value == highlight.locator.value

    async def test_lists_highlights_filtered_by_chapter(self, fake_uow) -> None:
        user_id = uuid4()
        book_id = uuid4()
        fake_uow.highlights.query.find_by_book.return_value = []

        use_case = ListHighlightsUseCase(uow=fake_uow)
        result = await use_case.execute(user_id, book_id, chapter=2)

        fake_uow.highlights.query.find_by_book.assert_awaited_once_with(user_id, book_id, 2)
        assert result == []