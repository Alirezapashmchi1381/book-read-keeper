import pytest

from tests.annotations.application.use_cases.factories import FakeAnnotationsUnitOfWork


@pytest.fixture
def fake_uow() -> FakeAnnotationsUnitOfWork:
    return FakeAnnotationsUnitOfWork()