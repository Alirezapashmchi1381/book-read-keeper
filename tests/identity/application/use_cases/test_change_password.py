import pytest

from src.identity.application.dtos.change_password_dto import ChangePasswordInputDto
from src.identity.application.use_cases.change_password import ChangePasswordUseCase
from tests.identity.application.use_cases.factories import FakePasswordHasher, make_user


@pytest.fixture
def use_case(fake_uow, fake_hasher) -> ChangePasswordUseCase:
    return ChangePasswordUseCase(uow=fake_uow, password_hasher=fake_hasher)


@pytest.fixture
def user():
    return make_user(password="old-password")


@pytest.fixture
def dto(user) -> ChangePasswordInputDto:
    return ChangePasswordInputDto(
        user_id=user.id.value,
        current_password="old-password",
        new_password="new-password",
    )


async def test_change_password_updates_hash(use_case, fake_uow, fake_hasher, user, dto):
    fake_uow.users.query.find_by_id.return_value = user

    await use_case.execute(dto)

    saved_user = fake_uow.users.command.save.call_args[0][0]
    assert saved_user.password_hash == fake_hasher.hash("new-password")


async def test_change_password_revokes_all_sessions(use_case, fake_uow, user, dto):
    fake_uow.users.query.find_by_id.return_value = user

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke_all_for_user.assert_called_once_with(dto.user_id)


async def test_change_password_raises_if_user_not_found(use_case, fake_uow, dto):
    fake_uow.users.query.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        await use_case.execute(dto)


async def test_change_password_raises_if_current_password_wrong(use_case, fake_uow, user, dto):
    fake_uow.users.query.find_by_id.return_value = user
    wrong_dto = ChangePasswordInputDto(
        user_id=dto.user_id,
        current_password="wrong",
        new_password="new-password",
    )

    with pytest.raises(ValueError, match="Current password is incorrect"):
        await use_case.execute(wrong_dto)


async def test_change_password_does_not_save_on_wrong_password(use_case, fake_uow, user, dto):
    fake_uow.users.query.find_by_id.return_value = user
    wrong_dto = ChangePasswordInputDto(
        user_id=dto.user_id,
        current_password="wrong",
        new_password="new-password",
    )

    with pytest.raises(ValueError):
        await use_case.execute(wrong_dto)

    fake_uow.users.command.save.assert_not_called()
