import pytest

from src.identity.application.dtos.verify_email_dto import VerifyEmailInputDto
from src.identity.application.use_cases.verify_email import VerifyEmailUseCase
from tests.identity.application.use_cases.factories import make_email_verification_token, make_user


@pytest.fixture
def use_case(fake_uow, fake_token_hasher) -> VerifyEmailUseCase:
    return VerifyEmailUseCase(uow=fake_uow, token_hasher=fake_token_hasher)


@pytest.fixture
def user():
    return make_user(is_verified=False)


@pytest.fixture
def verification_token(user):
    return make_email_verification_token(user_id=user.id, raw_token="fake-verification-token")


@pytest.fixture
def dto() -> VerifyEmailInputDto:
    return VerifyEmailInputDto(verification_token="fake-verification-token")


async def test_verify_email_marks_user_verified(use_case, fake_uow, user, verification_token, dto):
    fake_uow.email_verification_tokens.query.find_by_token_hash.return_value = verification_token
    fake_uow.users.query.find_by_id.return_value = user

    await use_case.execute(dto)

    saved_user = fake_uow.users.command.save.call_args[0][0]
    assert saved_user.is_verified is True


async def test_verify_email_deletes_token_after_use(use_case, fake_uow, user, verification_token, dto):
    fake_uow.email_verification_tokens.query.find_by_token_hash.return_value = verification_token
    fake_uow.users.query.find_by_id.return_value = user

    await use_case.execute(dto)

    fake_uow.email_verification_tokens.command.delete.assert_called_once_with(verification_token.id)


async def test_verify_email_raises_if_token_not_found(use_case, fake_uow, dto):
    fake_uow.email_verification_tokens.query.find_by_token_hash.return_value = None

    with pytest.raises(ValueError, match="Invalid or expired verification token"):
        await use_case.execute(dto)


async def test_verify_email_raises_if_token_expired(use_case, fake_uow, dto):
    expired = make_email_verification_token(raw_token=dto.verification_token, expired=True)
    fake_uow.email_verification_tokens.query.find_by_token_hash.return_value = expired

    with pytest.raises(ValueError, match="Invalid or expired verification token"):
        await use_case.execute(dto)


async def test_verify_email_raises_if_user_not_found(use_case, fake_uow, verification_token, dto):
    fake_uow.email_verification_tokens.query.find_by_token_hash.return_value = verification_token
    fake_uow.users.query.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        await use_case.execute(dto)
