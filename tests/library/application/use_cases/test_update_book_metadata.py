import pytest
from uuid import uuid4

from src.library.application.dtos.update_book_metadata_dto import UpdateBookMetadataInputDto
from src.library.application.use_cases.update_book_metadata import UpdateBookMetadataUseCase
from src.library.domain.exceptions import BookNotFoundError
from tests.library.application.use_cases.factories import make_book


@pytest.fixture
def use_case(fake_uow) -> UpdateBookMetadataUseCase:
    return UpdateBookMetadataUseCase(uow=fake_uow)


async def test_update_book_metadata_updates_title(use_case, fake_uow):
    book = make_book(title="Old Title")
    fake_uow.books.query.find_by_id.return_value = book

    dto = UpdateBookMetadataInputDto(
        book_id=book.id,
        title="New Title",
    )
    result = await use_case.execute(dto)

    assert result.metadata.title == "New Title"


async def test_update_book_metadata_updates_all_fields(use_case, fake_uow):
    book = make_book()
    fake_uow.books.query.find_by_id.return_value = book

    dto = UpdateBookMetadataInputDto(
        book_id=book.id,
        author_first_name="Jane",
        author_last_name="Austen",
        isbn="9780141439518",
        title="Pride and Prejudice",
        language="en",
        color="#123456",
        description="A classic novel.",
    )
    result = await use_case.execute(dto)

    assert result.metadata.author.first_name == "Jane"
    assert result.metadata.author.last_name == "Austen"
    assert result.metadata.isbn.value == "9780141439518"
    assert result.metadata.title == "Pride and Prejudice"


async def test_update_book_metadata_partial_update(use_case, fake_uow):
    book = make_book(title="Original Title", description="Original Description")
    fake_uow.books.query.find_by_id.return_value = book

    dto = UpdateBookMetadataInputDto(
        book_id=book.id,
        title="Updated Title Only",
    )
    result = await use_case.execute(dto)

    assert result.metadata.title == "Updated Title Only"
    assert result.metadata.description == "Original Description"


async def test_update_book_metadata_raises_if_not_found(use_case, fake_uow):
    fake_uow.books.query.find_by_id.return_value = None

    dto = UpdateBookMetadataInputDto(
        book_id=uuid4(),
        title="New Title",
    )
    with pytest.raises(BookNotFoundError):
        await use_case.execute(dto)


async def test_update_book_metadata_commits(use_case, fake_uow):
    book = make_book()
    fake_uow.books.query.find_by_id.return_value = book

    dto = UpdateBookMetadataInputDto(
        book_id=book.id,
        title="New Title",
    )
    await use_case.execute(dto)

    assert fake_uow.committed is True