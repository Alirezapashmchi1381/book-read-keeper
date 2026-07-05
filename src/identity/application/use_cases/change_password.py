from dataclasses import dataclass

from src.identity.application.dtos.change_password_dto import ChangePasswordInputDto
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork


@dataclass
class ChangePasswordUseCase:
    uow: IdentityUnitOfWork
    password_hasher: PasswordHasher

    async def execute(self, dto: ChangePasswordInputDto) -> None:
        async with self.uow as uow:
            user = await uow.users.query.find_by_id(dto.user_id)

            if user is None:
                raise ValueError("User not found")

            if not user.verify_password(dto.current_password, self.password_hasher):
                raise ValueError("Current password is incorrect")

            user.password_hash = self.password_hasher.hash(dto.new_password)
            await uow.users.command.save(user)

            # Force re-login on all devices after a password change
            await uow.refresh_tokens.command.revoke_all_for_user(dto.user_id)
