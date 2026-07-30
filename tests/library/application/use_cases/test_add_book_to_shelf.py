import pytest
from uuid import uuid4

from src.library.application.dtos.add_book_to_shelf_dto import AddBookToShelfInputDto
from src.library.application.use_cases.add_book_to_shelf import AddBookToShelfUseCase
from src.library.domain.exceptions import (
    BookNotFoundError,
    ShelfNotFoundError,
    DuplicateBookInShelfError,
)
from tests.library.application.use_cases.factories import make_book, make_shelf


@pytest.fixture
def use_case(fake_uow) -> AddBookToShelfUseCase:
    return AddBookToShelfUseCase(uow=fake_uow)


async def test_add_book_to_shelf_adds_book(use_case, fake_uow):
    book = make_book()
    shelf = make_shelf()
    fake_uow.books.query.find_by_id.return_value = book
    fake_uow.shelves.query.find_by_id.return_value = shelf

    dto = AddBookToShelfInputDto(shelf_id=shelf.id, book_id=book.id)
    result = await use_case.execute(dto)

    assert result.has_book(book.id) is True
    assert result.book_count() == 1


async def test_add_book_to_shelf_raises_if_book_not_found(use_case, fake_uow):
    shelf = make_shelf()
    fake_uow.books.query.find_by_id.return_value = None
    fake_uow.shelves.query.find_by_id.return_value = shelf

    dto = AddBookToShelfInputDto(shelf_id=shelf.id, book_id=uuid4())
    with pytest.raises(BookNotFoundError):
        await use_case.execute(dto)


async def test_add_book_to_shelf_raises_if_shelf_not_found(use_case, fake_uow):
    book = make_book()
    fake_uow.books.query.find_by_id.return_value = book
    fake_uow.shelves.query.find_by_id.return_value = None

    dto = AddBookToShelfInputDto(shelf_id=uuid4(), book_id=book.id)
    with pytest.raises(ShelfNotFoundError):
        await use_case.execute(dto)


async def test_add_book_to_shelf_raises_if_duplicate(use_case, fake_uow):
    book = make_book()
    shelf = make_shelf(book_ids=[book.id])
    fake_uow.books.query.find_by_id.return_value = book
    fake_uow.shelves.query.find_by_id.return_value = shelf

    dto = AddBookToShelfInputDto(shelf_id=shelf.id, book_id=book.id)
    with pytest.raises(DuplicateBookInShelfError):
        await use_case.execute(dto)


async def test_add_book_to_shelf_commits(use_case, fake_uow):
    book = make_book()
    shelf = make_shelf()
    fake_uow.books.query.find_by_id.return_value = book
    fake_uow.shelves.query.find_by_id.return_value = shelf

    dto = AddBookToShelfInputDto(shelf_id=shelf.id, book_id=book.id)
    await use_case.execute(dto)

    assert fake_uow.committed is True