import pytest

from tests.library.application.use_cases.factories import (
    FakeLibraryUnitOfWork,
    FakeFileStorageService,
)


@pytest.fixture
def fake_uow() -> FakeLibraryUnitOfWork:
    return FakeLibraryUnitOfWork()


@pytest.fixture
def fake_file_storage() -> FakeFileStorageService:
    return FakeFileStorageService()