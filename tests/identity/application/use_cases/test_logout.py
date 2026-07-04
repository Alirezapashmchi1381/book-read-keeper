import pytest

from src.identity.application.dtos.logout_dto import LogoutInputDto
from src.identity.application.use_cases.logout import LogoutUseCase
from tests.identity.application.use_cases.factories import make_refresh_token


@pytest.fixture
def use_case(fake_uow, fake_hasher) -> LogoutUseCase:
    return LogoutUseCase(uow=fake_uow, password_hasher=fake_hasher)


@pytest.fixture
def dto() -> LogoutInputDto:
    return LogoutInputDto(refresh_token="fake-refresh-token")


async def test_logout_revokes_valid_token(use_case, fake_uow, dto):
    token = make_refresh_token(raw_token=dto.refresh_token)
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = token

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke.assert_called_once_with(token.id)


async def test_logout_is_silent_when_token_not_found(use_case, fake_uow, dto):
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = None

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke.assert_not_called()


async def test_logout_is_silent_when_token_expired(use_case, fake_uow, dto):
    token = make_refresh_token(raw_token=dto.refresh_token, expired=True)
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = token

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke.assert_not_called()


async def test_logout_is_silent_when_token_already_revoked(use_case, fake_uow, dto):
    token = make_refresh_token(raw_token=dto.refresh_token, revoked=True)
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = token

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke.assert_not_called()
