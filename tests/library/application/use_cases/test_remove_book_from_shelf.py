import pytest
from uuid import uuid4

from src.library.application.dtos.remove_book_from_shelf_dto import RemoveBookFromShelfInputDto
from src.library.application.use_cases.remove_book_from_shelf import RemoveBookFromShelfUseCase
from src.library.domain.exceptions import (
    BookNotFoundError,
    ShelfNotFoundError,
    BookNotInShelfError,
)
from tests.library.application.use_cases.factories import make_book, make_shelf


@pytest.fixture
def use_case(fake_uow) -> RemoveBookFromShelfUseCase:
    return RemoveBookFromShelfUseCase(uow=fake_uow)


async def test_remove_book_from_shelf_removes_book(use_case, fake_uow):
    book = make_book()
    shelf = make_shelf(book_ids=[book.id])
    fake_uow.books.query.find_by_id.return_value = book
    fake_uow.shelves.query.find_by_id.return_value = shelf

    dto = RemoveBookFromShelfInputDto(shelf_id=shelf.id, book_id=book.id)
    result = await use_case.execute(dto)

    assert result.has_book(book.id) is False
    assert result.book_count() == 0


async def test_remove_book_from_shelf_raises_if_book_not_found(use_case, fake_uow):
    shelf = make_shelf()
    fake_uow.books.query.find_by_id.return_value = None
    fake_uow.shelves.query.find_by_id.return_value = shelf

    dto = RemoveBookFromShelfInputDto(shelf_id=shelf.id, book_id=uuid4())
    with pytest.raises(BookNotFoundError):
        await use_case.execute(dto)


async def test_remove_book_from_shelf_raises_if_shelf_not_found(use_case, fake_uow):
    book = make_book()
    fake_uow.books.query.find_by_id.return_value = book
    fake_uow.shelves.query.find_by_id.return_value = None

    dto = RemoveBookFromShelfInputDto(shelf_id=uuid4(), book_id=book.id)
    with pytest.raises(ShelfNotFoundError):
        await use_case.execute(dto)


async def test_remove_book_from_shelf_raises_if_not_in_shelf(use_case, fake_uow):
    book = make_book()
    shelf = make_shelf()
    fake_uow.books.query.find_by_id.return_value = book
    fake_uow.shelves.query.find_by_id.return_value = shelf

    dto = RemoveBookFromShelfInputDto(shelf_id=shelf.id, book_id=book.id)
    with pytest.raises(BookNotInShelfError):
        await use_case.execute(dto)


async def test_remove_book_from_shelf_commits(use_case, fake_uow):
    book = make_book()
    shelf = make_shelf(book_ids=[book.id])
    fake_uow.books.query.find_by_id.return_value = book
    fake_uow.shelves.query.find_by_id.return_value = shelf

    dto = RemoveBookFromShelfInputDto(shelf_id=shelf.id, book_id=book.id)
    await use_case.execute(dto)

    assert fake_uow.committed is True