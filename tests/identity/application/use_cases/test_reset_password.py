import pytest

from src.identity.domain.exceptions import InvalidTokenError, NotFoundError
from src.identity.application.dtos.reset_password_dto import ResetPasswordInputDto
from src.identity.application.use_cases.reset_password import ResetPasswordUseCase
from tests.identity.application.use_cases.factories import (
    FakePasswordHasher,
    make_password_reset_token,
    make_user,
)


@pytest.fixture
def use_case(fake_uow, fake_hasher, fake_token_hasher) -> ResetPasswordUseCase:
    return ResetPasswordUseCase(uow=fake_uow, password_hasher=fake_hasher, token_hasher=fake_token_hasher)


@pytest.fixture
def user():
    return make_user()


@pytest.fixture
def reset_token(user):
    return make_password_reset_token(user_id=user.id, raw_token="fake-reset-token")


@pytest.fixture
def dto() -> ResetPasswordInputDto:
    return ResetPasswordInputDto(reset_token="fake-reset-token", new_password="new-password")


async def test_reset_password_updates_hash(use_case, fake_uow, fake_hasher, user, reset_token, dto):
    fake_uow.password_reset_tokens.query.find_by_token_hash.return_value = reset_token
    fake_uow.users.query.find_by_id.return_value = user

    await use_case.execute(dto)

    saved_user = fake_uow.users.command.save.call_args[0][0]
    assert saved_user.password_hash == fake_hasher.hash("new-password")


async def test_reset_password_deletes_token_and_revokes_sessions(use_case, fake_uow, user, reset_token, dto):
    fake_uow.password_reset_tokens.query.find_by_token_hash.return_value = reset_token
    fake_uow.users.query.find_by_id.return_value = user

    await use_case.execute(dto)

    fake_uow.password_reset_tokens.command.delete.assert_called_once_with(reset_token.id)
    fake_uow.refresh_tokens.command.revoke_all_for_user.assert_called_once_with(reset_token.user_id)


async def test_reset_password_raises_if_token_not_found(use_case, fake_uow, dto):
    fake_uow.password_reset_tokens.query.find_by_token_hash.return_value = None

    with pytest.raises(InvalidTokenError, match="Invalid or expired reset token"):
        await use_case.execute(dto)


async def test_reset_password_raises_if_token_expired(use_case, fake_uow, dto):
    expired = make_password_reset_token(raw_token=dto.reset_token, expired=True)
    fake_uow.password_reset_tokens.query.find_by_token_hash.return_value = expired

    with pytest.raises(InvalidTokenError, match="Invalid or expired reset token"):
        await use_case.execute(dto)


async def test_reset_password_raises_if_user_not_found(use_case, fake_uow, reset_token, dto):
    fake_uow.password_reset_tokens.query.find_by_token_hash.return_value = reset_token
    fake_uow.users.query.find_by_id.return_value = None

    with pytest.raises(NotFoundError, match="User not found"):
        await use_case.execute(dto)
