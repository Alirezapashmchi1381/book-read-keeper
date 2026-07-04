from uuid import uuid4

import pytest

from src.identity.application.dtos.logout_dto import LogoutAllDevicesInputDto
from src.identity.application.use_cases.logout_all_devices import LogoutAllDevicesUseCase


@pytest.fixture
def use_case(fake_uow) -> LogoutAllDevicesUseCase:
    return LogoutAllDevicesUseCase(uow=fake_uow)


async def test_logout_all_devices_revokes_all_user_tokens(use_case, fake_uow):
    user_id = uuid4()
    dto = LogoutAllDevicesInputDto(user_id=user_id)

    await use_case.execute(dto)

    fake_uow.refresh_tokens.command.revoke_all_for_user.assert_called_once_with(user_id)
