import pytest

from src.identity.domain.exceptions import NotFoundError
from src.identity.application.dtos.verify_email_dto import RequestEmailVerificationInputDto
from src.identity.application.use_cases.request_email_verification import RequestEmailVerificationUseCase
from tests.identity.application.use_cases.factories import make_user


@pytest.fixture
def use_case(fake_uow, fake_token_hasher, fake_secret_generator, fake_email_service) -> RequestEmailVerificationUseCase:
    return RequestEmailVerificationUseCase(
        uow=fake_uow,
        token_hasher=fake_token_hasher,
        secret_generator=fake_secret_generator,
        email_service=fake_email_service,
    )


@pytest.fixture
def unverified_user():
    return make_user(email="alice@example.com", is_verified=False)


@pytest.fixture
def dto(unverified_user) -> RequestEmailVerificationInputDto:
    return RequestEmailVerificationInputDto(user_id=str(unverified_user.id))


async def test_sends_verification_email(use_case, fake_uow, fake_email_service, unverified_user, dto):
    fake_uow.users.query.find_by_id.return_value = unverified_user

    await use_case.execute(dto)

    assert len(fake_email_service.sent_verification) == 1
    assert fake_email_service.sent_verification[0][0] == unverified_user.email.address


async def test_deletes_old_tokens_before_saving_new(use_case, fake_uow, unverified_user, dto):
    fake_uow.users.query.find_by_id.return_value = unverified_user

    await use_case.execute(dto)

    fake_uow.email_verification_tokens.command.delete_all_for_user.assert_called_once_with(
        unverified_user.id
    )
    fake_uow.email_verification_tokens.command.save.assert_called_once()


async def test_is_silent_if_user_already_verified(use_case, fake_uow, fake_email_service, dto):
    verified_user = make_user(email="alice@example.com", is_verified=True)
    fake_uow.users.query.find_by_id.return_value = verified_user

    await use_case.execute(dto)

    fake_uow.email_verification_tokens.command.save.assert_not_called()
    assert fake_email_service.sent_verification == []


async def test_raises_if_user_not_found(use_case, fake_uow, dto):
    fake_uow.users.query.find_by_id.return_value = None

    with pytest.raises(NotFoundError, match="User not found"):
        await use_case.execute(dto)
