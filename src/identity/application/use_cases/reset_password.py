from dataclasses import dataclass
from datetime import datetime

from src.identity.application.dtos.reset_password_dto import ResetPasswordInputDto
from src.identity.domain.exceptions import InvalidTokenError, NotFoundError
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.token_hasher import TokenHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork


@dataclass
class ResetPasswordUseCase:
    uow: IdentityUnitOfWork
    password_hasher: PasswordHasher
    token_hasher: TokenHasher

    async def execute(self, dto: ResetPasswordInputDto) -> None:
        async with self.uow as uow:
            token_hash = self.token_hasher.hash(dto.reset_token)
            reset_token = await uow.password_reset_tokens.query.find_by_token_hash(token_hash)

            if reset_token is None or reset_token.is_expired(datetime.now()):
                raise InvalidTokenError("Invalid or expired reset token")

            user = await uow.users.query.find_by_id(reset_token.user_id)
            if user is None:
                raise NotFoundError("User not found")

            user.password_hash = self.password_hasher.hash(dto.new_password)
            await uow.users.command.save(user)

            # Consume the token and force re-login everywhere
            await uow.password_reset_tokens.command.delete(reset_token.id)
            await uow.refresh_tokens.command.revoke_all_for_user(reset_token.user_id)
