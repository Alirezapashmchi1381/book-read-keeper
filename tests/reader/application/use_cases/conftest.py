import pytest

from tests.reader.application.use_cases.factories import FakeReaderUnitOfWork


@pytest.fixture
def fake_uow() -> FakeReaderUnitOfWork:
    return FakeReaderUnitOfWork()