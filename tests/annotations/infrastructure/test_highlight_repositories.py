from uuid import uuid4

import pytest

from src.annotations.infrastructure.sql.repository.sqlalchemy_highlight_command_repository import (
    SQLAlchemyHighlightCommandRepository,
)
from src.annotations.infrastructure.sql.repository.sqlalchemy_highlight_query_repository import (
    SQLAlchemyHighlightQueryRepository,
)

from tests.annotations.infrastructure.factories import make_highlight


@pytest.mark.asyncio
class TestHighlightCommandRepository:
    async def test_save_and_find_by_id(self, session) -> None:
        command = SQLAlchemyHighlightCommandRepository(session)
        highlight = make_highlight(selected_text="hello", note="note")
        await command.save(highlight)
        await session.commit()

        query = SQLAlchemyHighlightQueryRepository(session)
        found = await query.find_by_id(highlight.id)

        assert found is not None
        assert found.id == highlight.id
        assert found.selected_text == "hello"
        assert found.note is not None
        assert found.note.value == "note"
        assert found.locator.chapter is not None
        assert found.locator.chapter.number == 1

    async def test_delete(self, session) -> None:
        command = SQLAlchemyHighlightCommandRepository(session)
        highlight = make_highlight()
        await command.save(highlight)
        await session.commit()

        await command.delete(highlight)
        await session.commit()

        query = SQLAlchemyHighlightQueryRepository(session)
        found = await query.find_by_id(highlight.id)
        assert found is None


@pytest.mark.asyncio
class TestHighlightQueryRepository:
    async def test_find_by_book(self, session) -> None:
        command = SQLAlchemyHighlightCommandRepository(session)
        user_id = uuid4()
        book_id = uuid4()
        h1 = make_highlight(book_id=book_id, user_id=user_id, selected_text="first")
        h2 = make_highlight(book_id=book_id, user_id=user_id, selected_text="second")
        other = make_highlight(selected_text="other book")
        await command.save(h1)
        await command.save(h2)
        await command.save(other)
        await session.commit()

        query = SQLAlchemyHighlightQueryRepository(session)
        results = await query.find_by_book(user_id, book_id)

        assert len(results) == 2
        assert {r.selected_text for r in results} == {"first", "second"}

    async def test_find_by_book_filtered_by_chapter(self, session) -> None:
        command = SQLAlchemyHighlightCommandRepository(session)
        user_id = uuid4()
        book_id = uuid4()
        ch1 = make_highlight(book_id=book_id, user_id=user_id, chapter_number=1)
        ch2 = make_highlight(book_id=book_id, user_id=user_id, chapter_number=2)
        await command.save(ch1)
        await command.save(ch2)
        await session.commit()

        query = SQLAlchemyHighlightQueryRepository(session)
        results = await query.find_by_book(user_id, book_id, chapter=2)

        assert len(results) == 1
        assert results[0].locator.chapter is not None
        assert results[0].locator.chapter.number == 2

    async def test_list_by_user(self, session) -> None:
        command = SQLAlchemyHighlightCommandRepository(session)
        user_id = uuid4()
        await command.save(make_highlight(user_id=user_id))
        await command.save(make_highlight(user_id=user_id))
        await command.save(make_highlight(user_id=uuid4()))
        await session.commit()

        query = SQLAlchemyHighlightQueryRepository(session)
        results = await query.list_by_user(user_id)

        assert len(results) == 2

    async def test_find_by_id_returns_none_when_missing(self, session) -> None:
        query = SQLAlchemyHighlightQueryRepository(session)
        found = await query.find_by_id(uuid4())
        assert found is None