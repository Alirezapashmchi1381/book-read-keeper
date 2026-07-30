import pytest
from uuid import uuid4

from src.library.application.use_cases.restore_book import RestoreBookUseCase
from src.library.domain.exceptions import BookNotFoundError, BookNotDeletedError
from tests.library.application.use_cases.factories import make_book


@pytest.fixture
def use_case(fake_uow) -> RestoreBookUseCase:
    return RestoreBookUseCase(uow=fake_uow)


async def test_restore_book_restores_deleted_book(use_case, fake_uow):
    book = make_book(is_deleted=True)
    fake_uow.books.query.find_by_id.return_value = book

    await use_case.execute(book.id)

    assert book.is_deleted is False
    assert book.deleted_at is None


async def test_restore_book_raises_if_not_found(use_case, fake_uow):
    fake_uow.books.query.find_by_id.return_value = None

    with pytest.raises(BookNotFoundError):
        await use_case.execute(uuid4())


async def test_restore_book_raises_if_not_deleted(use_case, fake_uow):
    book = make_book(is_deleted=False)
    fake_uow.books.query.find_by_id.return_value = book

    with pytest.raises(BookNotDeletedError):
        await use_case.execute(book.id)


async def test_restore_book_commits(use_case, fake_uow):
    book = make_book(is_deleted=True)
    fake_uow.books.query.find_by_id.return_value = book

    await use_case.execute(book.id)

    assert fake_uow.committed is True