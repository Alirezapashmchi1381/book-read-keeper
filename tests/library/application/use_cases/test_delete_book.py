import pytest
from uuid import uuid4

from src.library.application.use_cases.delete_book import DeleteBookUseCase
from src.library.domain.exceptions import BookNotFoundError, BookAlreadyDeletedError
from tests.library.application.use_cases.factories import make_book


@pytest.fixture
def use_case(fake_uow) -> DeleteBookUseCase:
    return DeleteBookUseCase(uow=fake_uow)


async def test_delete_book_soft_deletes(use_case, fake_uow):
    book = make_book(is_deleted=False)
    fake_uow.books.query.find_by_id.return_value = book

    await use_case.execute(book.id)

    assert book.is_deleted is True
    assert book.deleted_at is not None


async def test_delete_book_raises_if_not_found(use_case, fake_uow):
    fake_uow.books.query.find_by_id.return_value = None

    with pytest.raises(BookNotFoundError):
        await use_case.execute(uuid4())


async def test_delete_book_raises_if_already_deleted(use_case, fake_uow):
    book = make_book(is_deleted=True)
    fake_uow.books.query.find_by_id.return_value = book

    with pytest.raises(BookAlreadyDeletedError):
        await use_case.execute(book.id)


async def test_delete_book_commits(use_case, fake_uow):
    book = make_book(is_deleted=False)
    fake_uow.books.query.find_by_id.return_value = book

    await use_case.execute(book.id)

    assert fake_uow.committed is True