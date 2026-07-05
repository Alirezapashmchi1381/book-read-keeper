import pytest

from src.identity.application.dtos.login_dto import LoginInputDto
from src.identity.application.use_cases.login import LoginUseCase
from tests.identity.application.use_cases.factories import make_user # type: ignore


@pytest.fixture
def use_case(fake_uow, fake_hasher, fake_token_hasher, fake_tokens, fake_secret_generator) -> LoginUseCase:
    return LoginUseCase(
        uow=fake_uow,
        password_hasher=fake_hasher,
        token_hasher=fake_token_hasher,
        token_service=fake_tokens,
        secret_generator=fake_secret_generator,
    )


@pytest.fixture
def dto() -> LoginInputDto:
    return LoginInputDto(email="alice@example.com", password="secret123")


@pytest.fixture
def active_user():
    return make_user(email="alice@example.com", password="secret123", is_active=True)


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

async def test_login_returns_auth_result(use_case, fake_uow, dto, active_user):
    fake_uow.users.query.find_by_email.return_value = active_user

    result = await use_case.execute(dto)

    assert result.email == dto.email
    assert result.access_token == "fake-access-token"
    assert result.refresh_token == "fake-refresh-token"


async def test_login_revokes_old_tokens_and_saves_new(use_case, fake_uow, dto, active_user):
    fake_uow.users.query.find_by_email.return_value = active_user

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke_all_for_user.assert_called_once_with(active_user.id)
    fake_uow.refresh_tokens.command.save.assert_called_once()


async def test_login_commits_transaction(use_case, fake_uow, dto, active_user):
    fake_uow.users.query.find_by_email.return_value = active_user

    await use_case.execute(dto)

    assert fake_uow.committed is True


# ---------------------------------------------------------------------------
# Auth failures — all surface as the same generic message (no email enumeration)
# ---------------------------------------------------------------------------

async def test_login_raises_if_user_not_found(use_case, fake_uow, dto):
    fake_uow.users.query.find_by_email.return_value = None

    with pytest.raises(ValueError, match="Invalid credentials"):
        await use_case.execute(dto)


async def test_login_raises_if_wrong_password(use_case, fake_uow, dto, active_user):
    fake_uow.users.query.find_by_email.return_value = active_user
    wrong_dto = LoginInputDto(email=dto.email, password="wrong-password")

    with pytest.raises(ValueError, match="Invalid credentials"):
        await use_case.execute(wrong_dto)


async def test_login_raises_if_account_deactivated(use_case, fake_uow, dto):
    inactive_user = make_user(email="alice@example.com", password="secret123")
    inactive_user.deactivate()
    fake_uow.users.query.find_by_email.return_value = inactive_user

    with pytest.raises(ValueError, match="Account is deactivated"):
        await use_case.execute(dto)
