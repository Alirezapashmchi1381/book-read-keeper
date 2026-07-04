import pytest

from src.identity.application.dtos.request_password_reset_dto import RequestPasswordResetInputDto
from src.identity.application.use_cases.request_password_reset import RequestPasswordResetUseCase
from tests.identity.application.use_cases.factories import make_user


@pytest.fixture
def use_case(fake_uow, fake_hasher, fake_tokens, fake_email_service) -> RequestPasswordResetUseCase:
    return RequestPasswordResetUseCase(
        uow=fake_uow,
        password_hasher=fake_hasher,
        token_service=fake_tokens,
        email_service=fake_email_service,
    )


@pytest.fixture
def user():
    return make_user(email="alice@example.com")


@pytest.fixture
def dto() -> RequestPasswordResetInputDto:
    return RequestPasswordResetInputDto(email="alice@example.com")


async def test_sends_reset_email(use_case, fake_uow, fake_email_service, user, dto):
    fake_uow.users.query.find_by_email.return_value = user

    await use_case.execute(dto)

    assert len(fake_email_service.sent_reset) == 1
    assert fake_email_service.sent_reset[0][0] == user.email.address


async def test_deletes_old_tokens_before_saving_new(use_case, fake_uow, user, dto):
    fake_uow.users.query.find_by_email.return_value = user

    await use_case.execute(dto)

    fake_uow.password_reset_tokens.command.delete_all_for_user.assert_called_once_with(user.id.value)
    fake_uow.password_reset_tokens.command.save.assert_called_once()


async def test_is_silent_if_email_not_registered(use_case, fake_uow, fake_email_service, dto):
    fake_uow.users.query.find_by_email.return_value = None

    await use_case.execute(dto)

    fake_uow.password_reset_tokens.command.save.assert_not_called()
    assert fake_email_service.sent_reset == []
