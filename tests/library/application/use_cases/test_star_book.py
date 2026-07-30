import pytest
from uuid import uuid4

from src.library.application.use_cases.star_book import StarBookUseCase
from src.library.domain.exceptions import BookNotFoundError
from tests.library.application.use_cases.factories import make_book


@pytest.fixture
def use_case(fake_uow) -> StarBookUseCase:
    return StarBookUseCase(uow=fake_uow)


async def test_star_book_toggles_star(use_case, fake_uow):
    book = make_book(is_starred=False)
    fake_uow.books.query.find_by_id.return_value = book

    result = await use_case.execute(book.id)

    assert result.is_starred is True


async def test_star_book_toggles_unstar(use_case, fake_uow):
    book = make_book(is_starred=True)
    fake_uow.books.query.find_by_id.return_value = book

    result = await use_case.execute(book.id)

    assert result.is_starred is False


async def test_star_book_raises_if_not_found(use_case, fake_uow):
    fake_uow.books.query.find_by_id.return_value = None

    with pytest.raises(BookNotFoundError):
        await use_case.execute(uuid4())


async def test_star_book_commits(use_case, fake_uow):
    book = make_book()
    fake_uow.books.query.find_by_id.return_value = book

    await use_case.execute(book.id)

    assert fake_uow.committed is True