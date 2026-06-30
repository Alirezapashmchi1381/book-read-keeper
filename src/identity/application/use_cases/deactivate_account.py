from dataclasses import dataclass
from typing import Callable

from src.identity.application.dtos.deactivate_account_dto import DeactivateAccountInputDto
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.user_id import UserId


@dataclass
class DeactivateAccountUseCase:
    uow_factory: Callable[[], IdentityUnitOfWork]

    async def execute(self, dto: DeactivateAccountInputDto) -> None:
        async with self.uow_factory() as uow:
            user = await uow.user_query.find_by_id(UserId(dto.user_id))

            if user is None:
                raise ValueError("User not found")

            user.deactivate()
            await uow.user_command.save(user)

            await uow.refresh_token_command.revoke_all_for_user(dto.user_id)
