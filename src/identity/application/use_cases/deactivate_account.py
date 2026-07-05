from dataclasses import dataclass

from src.identity.application.dtos.deactivate_account_dto import DeactivateAccountInputDto
from src.identity.domain.exceptions import NotFoundError
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork


@dataclass
class DeactivateAccountUseCase:
    uow: IdentityUnitOfWork

    async def execute(self, dto: DeactivateAccountInputDto) -> None:
        async with self.uow as uow:
            user = await uow.users.query.find_by_id(dto.user_id)

            if user is None:
                raise NotFoundError("User not found")

            user.deactivate()
            await uow.users.command.save(user)

            await uow.refresh_tokens.command.revoke_all_for_user(dto.user_id)
