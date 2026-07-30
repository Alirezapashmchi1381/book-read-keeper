import pytest

from src.library.application.dtos.create_book_dto import CreateBookInputDto
from src.library.application.use_cases.create_book import CreateBookUseCase
from src.library.domain.entities.book import Book


@pytest.fixture
def use_case(fake_uow) -> CreateBookUseCase:
    return CreateBookUseCase(uow=fake_uow)


@pytest.fixture
def valid_dto() -> CreateBookInputDto:
    return CreateBookInputDto(
        author_first_name="J.K.",
        author_last_name="Rowling",
        isbn="9780747532699",
        title="Harry Potter and the Philosopher's Stone",
        language="en",
        color="#740001",
        description="A young wizard's first year at Hogwarts.",
    )


async def test_create_book_returns_book(use_case, fake_uow, valid_dto):
    fake_uow.books.query.find_by_id.return_value = None

    result = await use_case.execute(valid_dto)

    assert isinstance(result, Book)
    assert result.metadata.title == valid_dto.title
    assert result.metadata.author.first_name == valid_dto.author_first_name
    assert result.metadata.author.last_name == valid_dto.author_last_name
    assert result.metadata.isbn.value == valid_dto.isbn


async def test_create_book_saves_book(use_case, fake_uow, valid_dto):
    await use_case.execute(valid_dto)

    fake_uow.books.command.save.assert_called_once()
    saved_book = fake_uow.books.command.save.call_args[0][0]
    assert saved_book.metadata.title == valid_dto.title


async def test_create_book_commits_transaction(use_case, fake_uow, valid_dto):
    await use_case.execute(valid_dto)

    assert fake_uow.committed is True


async def test_create_book_generates_uuid(use_case, fake_uow, valid_dto):
    await use_case.execute(valid_dto)

    saved_book = fake_uow.books.command.save.call_args[0][0]
    assert saved_book.id is not None