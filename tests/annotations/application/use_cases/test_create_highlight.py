from uuid import uuid4

from src.annotations.application.dtos.create_highlight_dto import CreateHighlightInputDto
from src.annotations.application.use_cases.create_highlight import CreateHighlightUseCase


class TestCreateHighlightUseCase:
    async def test_creates_and_saves_highlight(self, fake_uow) -> None:
        user_id = uuid4()
        book_id = uuid4()
        use_case = CreateHighlightUseCase(uow=fake_uow)

        highlight = await use_case.execute(
            CreateHighlightInputDto(
                user_id=user_id,
                book_id=book_id,
                selected_text="hello world",
                color="#FF5733",
                start_value="cfi-1",
                start_provider="epub",
                start_sort_key="1.0",
                start_chapter_number=1,
                start_chapter_title="Chapter 1",
                end_value="cfi-2",
                end_provider="epub",
                end_sort_key="1.1",
                end_chapter_number=1,
                end_chapter_title="Chapter 1",
                note="my note",
            )
        )

        assert highlight.id is not None
        assert highlight.user_id == user_id
        assert highlight.locator.book_id == book_id
        assert highlight.locator.chapter is not None
        assert highlight.locator.chapter.number == 1
        assert highlight.note is not None
        assert highlight.note.value == "my note"
        fake_uow.highlights.command.save.assert_awaited_once_with(highlight)
        assert fake_uow.committed is True

    async def test_creates_highlight_without_chapter(self, fake_uow) -> None:
        user_id = uuid4()
        book_id = uuid4()
        use_case = CreateHighlightUseCase(uow=fake_uow)

        highlight = await use_case.execute(
            CreateHighlightInputDto(
                user_id=user_id,
                book_id=book_id,
                selected_text="text",
                color="#FF5733",
                start_value="page:1",
                start_provider="pdf",
                start_sort_key="1.0",
                end_value="page:1",
                end_provider="pdf",
                end_sort_key="1.2",
            )
        )

        assert highlight.locator.chapter is None
        assert highlight.end_locator.chapter is None
        fake_uow.highlights.command.save.assert_awaited_once_with(highlight)