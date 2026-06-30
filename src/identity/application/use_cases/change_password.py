from dataclasses import dataclass
from typing import Callable

from src.identity.application.dtos.change_password_dto import ChangePasswordInputDto
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.user_id import UserId


@dataclass
class ChangePasswordUseCase:
    uow_factory: Callable[[], IdentityUnitOfWork]
    password_hasher: PasswordHasher

    async def execute(self, dto: ChangePasswordInputDto) -> None:
        async with self.uow_factory() as uow:
            user = await uow.user_query.find_by_id(UserId(dto.user_id))

            if user is None:
                raise ValueError("User not found")

            if not self.password_hasher.verify(dto.current_password, user.password_hash):
                raise ValueError("Current password is incorrect")

            user.password_hash = self.password_hasher.hash(dto.new_password)
            await uow.user_command.save(user)

            # Force re-login on all devices after a password change
            await uow.refresh_token_command.revoke_all_for_user(dto.user_id)
