import pytest

from src.identity.domain.exceptions import InvalidTokenError
from src.identity.application.dtos.refresh_token_dto import RefreshTokenInputDto
from src.identity.application.use_cases.refresh_token import RefreshTokenUseCase
from tests.identity.application.use_cases.factories import make_refresh_token


@pytest.fixture
def use_case(fake_uow, fake_token_hasher, fake_tokens, fake_secret_generator) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(
        uow=fake_uow,
        token_hasher=fake_token_hasher,
        token_service=fake_tokens,
        secret_generator=fake_secret_generator,
    )


@pytest.fixture
def dto() -> RefreshTokenInputDto:
    return RefreshTokenInputDto(refresh_token="fake-refresh-token")


@pytest.fixture
def valid_token():
    return make_refresh_token(raw_token="fake-refresh-token")


async def test_refresh_token_returns_new_tokens(use_case, fake_uow, dto, valid_token):
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = valid_token

    result = await use_case.execute(dto)

    assert result.access_token == "fake-access-token"
    assert result.refresh_token == "fake-refresh-token"


async def test_refresh_token_revokes_old_and_saves_new(use_case, fake_uow, dto, valid_token):
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = valid_token

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke.assert_called_once_with(valid_token.id)
    fake_uow.refresh_tokens.command.save.assert_called_once()


async def test_refresh_token_raises_if_token_not_found(use_case, fake_uow, dto):
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = None

    with pytest.raises(InvalidTokenError, match="Invalid or expired refresh token"):
        await use_case.execute(dto)


async def test_refresh_token_raises_if_token_expired(use_case, fake_uow, dto):
    expired = make_refresh_token(raw_token=dto.refresh_token, expired=True)
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = expired

    with pytest.raises(InvalidTokenError, match="Invalid or expired refresh token"):
        await use_case.execute(dto)


async def test_refresh_token_raises_if_token_revoked(use_case, fake_uow, dto):
    revoked = make_refresh_token(raw_token=dto.refresh_token, revoked=True)
    fake_uow.refresh_tokens.query.find_by_token_hash.return_value = revoked

    with pytest.raises(InvalidTokenError, match="Invalid or expired refresh token"):
        await use_case.execute(dto)
