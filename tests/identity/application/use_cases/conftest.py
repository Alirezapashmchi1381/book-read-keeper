import pytest

from tests.identity.application.use_cases.factories import ( # type: ignore
    FakeEmailService,
    FakeIdentityUnitOfWork,
    FakePasswordHasher,
    FakeTokenHasher,
    FakeTokenService,
)


@pytest.fixture
def fake_uow() -> FakeIdentityUnitOfWork:
    return FakeIdentityUnitOfWork()


@pytest.fixture
def fake_hasher() -> FakePasswordHasher:
    return FakePasswordHasher()


@pytest.fixture
def fake_token_hasher() -> FakeTokenHasher:
    return FakeTokenHasher()


@pytest.fixture
def fake_tokens() -> FakeTokenService:
    return FakeTokenService()


@pytest.fixture
def fake_email_service() -> FakeEmailService:
    return FakeEmailService()
