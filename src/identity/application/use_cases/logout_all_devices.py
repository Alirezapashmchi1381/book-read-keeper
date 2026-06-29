from dataclasses import dataclass

from src.identity.application.dtos.logout_dto import LogoutAllDevicesInputDto
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork


@dataclass
class LogoutAllDevicesUseCase:
    uow: IdentityUnitOfWork

    async def execute(self, dto: LogoutAllDevicesInputDto) -> None:
        async with self.uow as uow:
            await uow.refresh_token_command.revoke_all_for_user(dto.user_id)
