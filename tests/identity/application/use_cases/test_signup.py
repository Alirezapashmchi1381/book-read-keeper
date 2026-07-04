import pytest

from src.identity.application.dtos.signup_dto import SignupInputDto
from src.identity.application.use_cases.signup import SignupUseCase
from tests.identity.application.use_cases.factories import ( # type: ignore
    FakeIdentityUnitOfWork,
    FakePasswordHasher,
    FakeTokenService,
)


@pytest.fixture
def use_case(fake_uow, fake_hasher, fake_tokens) -> SignupUseCase:
    return SignupUseCase(uow=fake_uow, password_hasher=fake_hasher, token_service=fake_tokens)


@pytest.fixture
def valid_dto() -> SignupInputDto:
    return SignupInputDto(email="alice@example.com", username="alice", password="secret123")


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

async def test_signup_returns_auth_result(use_case, fake_uow, valid_dto):
    fake_uow.users.query.exists_by_email.return_value = False
    fake_uow.users.query.exists_by_username.return_value = False

    result = await use_case.execute(valid_dto)

    assert result.email == valid_dto.email
    assert result.username == valid_dto.username
    assert result.access_token == "fake-access-token"
    assert result.refresh_token == "fake-refresh-token"


async def test_signup_saves_user_and_refresh_token(use_case, fake_uow, valid_dto):
    fake_uow.users.query.exists_by_email.return_value = False
    fake_uow.users.query.exists_by_username.return_value = False

    await use_case.execute(valid_dto)

    fake_uow.users.command.save.assert_called_once()
    fake_uow.refresh_tokens.command.save.assert_called_once()


async def test_signup_hashes_password(use_case, fake_uow, fake_hasher, valid_dto):
    fake_uow.users.query.exists_by_email.return_value = False
    fake_uow.users.query.exists_by_username.return_value = False

    await use_case.execute(valid_dto)

    saved_user = fake_uow.users.command.save.call_args[0][0]
    assert saved_user.password_hash == fake_hasher.hash(valid_dto.password)


async def test_signup_commits_transaction(use_case, fake_uow, valid_dto):
    fake_uow.users.query.exists_by_email.return_value = False
    fake_uow.users.query.exists_by_username.return_value = False

    await use_case.execute(valid_dto)

    assert fake_uow.committed is True


# ---------------------------------------------------------------------------
# Duplicate checks
# ---------------------------------------------------------------------------

async def test_signup_raises_if_email_taken(use_case, fake_uow, valid_dto):
    fake_uow.users.query.exists_by_email.return_value = True

    with pytest.raises(ValueError, match="Email is already registered"):
        await use_case.execute(valid_dto)


async def test_signup_raises_if_username_taken(use_case, fake_uow, valid_dto):
    fake_uow.users.query.exists_by_email.return_value = False
    fake_uow.users.query.exists_by_username.return_value = True

    with pytest.raises(ValueError, match="Username is already taken"):
        await use_case.execute(valid_dto)


async def test_signup_does_not_save_on_duplicate_email(use_case, fake_uow, valid_dto):
    fake_uow.users.query.exists_by_email.return_value = True

    with pytest.raises(ValueError):
        await use_case.execute(valid_dto)

    fake_uow.users.command.save.assert_not_called()
