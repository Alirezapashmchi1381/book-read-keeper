import pytest

from src.identity.application.dtos.deactivate_account_dto import DeactivateAccountInputDto
from src.identity.application.use_cases.deactivate_account import DeactivateAccountUseCase
from tests.identity.application.use_cases.factories import make_user


@pytest.fixture
def use_case(fake_uow) -> DeactivateAccountUseCase:
    return DeactivateAccountUseCase(uow=fake_uow)


@pytest.fixture
def user():
    return make_user()


@pytest.fixture
def dto(user) -> DeactivateAccountInputDto:
    return DeactivateAccountInputDto(user_id=user.id)


async def test_deactivate_account_marks_user_inactive(use_case, fake_uow, user, dto):
    fake_uow.users.query.find_by_id.return_value = user

    await use_case.execute(dto)

    saved_user = fake_uow.users.command.save.call_args[0][0]
    assert saved_user.is_active is False


async def test_deactivate_account_revokes_all_sessions(use_case, fake_uow, user, dto):
    fake_uow.users.query.find_by_id.return_value = user

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke_all_for_user.assert_called_once_with(dto.user_id)


async def test_deactivate_account_raises_if_user_not_found(use_case, fake_uow, dto):
    fake_uow.users.query.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        await use_case.execute(dto)
