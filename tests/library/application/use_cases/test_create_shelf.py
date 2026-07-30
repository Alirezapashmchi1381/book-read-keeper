import pytest

from src.library.application.dtos.create_shelf_dto import CreateShelfInputDto
from src.library.application.use_cases.create_shelf import CreateShelfUseCase
from src.library.domain.entities.shelf import Shelf


@pytest.fixture
def use_case(fake_uow) -> CreateShelfUseCase:
    return CreateShelfUseCase(uow=fake_uow)


@pytest.fixture
def valid_dto() -> CreateShelfInputDto:
    return CreateShelfInputDto(name="Favorites", color="#FF5733")


async def test_create_shelf_returns_shelf(use_case, fake_uow, valid_dto):
    result = await use_case.execute(valid_dto)

    assert isinstance(result, Shelf)
    assert result.name.name == valid_dto.name
    assert result.color.hex_value == valid_dto.color


async def test_create_shelf_saves_shelf(use_case, fake_uow, valid_dto):
    await use_case.execute(valid_dto)

    fake_uow.shelves.command.save.assert_called_once()
    saved_shelf = fake_uow.shelves.command.save.call_args[0][0]
    assert saved_shelf.name.name == valid_dto.name


async def test_create_shelf_commits(use_case, fake_uow, valid_dto):
    await use_case.execute(valid_dto)

    assert fake_uow.committed is True


async def test_create_shelf_has_no_books_by_default(use_case, fake_uow, valid_dto):
    result = await use_case.execute(valid_dto)

    assert result.book_count() == 0