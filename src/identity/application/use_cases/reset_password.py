from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from src.identity.application.dtos.reset_password_dto import ResetPasswordInputDto
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.user_id import UserId


@dataclass
class ResetPasswordUseCase:
    uow_factory: Callable[[], IdentityUnitOfWork]
    password_hasher: PasswordHasher

    async def execute(self, dto: ResetPasswordInputDto) -> None:
        async with self.uow_factory() as uow:
            token_hash = self.password_hasher.hash(dto.reset_token)
            reset_token = await uow.password_reset_token_query.find_by_token_hash(token_hash)

            if reset_token is None or reset_token.is_expired(datetime.now()):
                raise ValueError("Invalid or expired reset token")

            user = await uow.user_query.find_by_id(UserId(reset_token.user_id))
            if user is None:
                raise ValueError("User not found")

            user.password_hash = self.password_hasher.hash(dto.new_password)
            await uow.user_command.save(user)

            # Consume the token and force re-login everywhere
            await uow.password_reset_token_command.delete(reset_token.id)
            await uow.refresh_token_command.revoke_all_for_user(reset_token.user_id)
