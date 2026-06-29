from dataclasses import dataclass
from datetime import datetime

from src.identity.application.dtos.verify_email_dto import VerifyEmailInputDto
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.user_id import UserId


@dataclass
class VerifyEmailUseCase:
    uow: IdentityUnitOfWork
    password_hasher: PasswordHasher

    async def execute(self, dto: VerifyEmailInputDto) -> None:
        async with self.uow as uow:
            token_hash = self.password_hasher.hash(dto.verification_token)
            verification_token = await uow.email_verification_token_query.find_by_token_hash(token_hash)

            if verification_token is None or verification_token.is_expired(datetime.now()):
                raise ValueError("Invalid or expired verification token")

            user = await uow.user_query.find_by_id(UserId(verification_token.user_id))
            if user is None:
                raise ValueError("User not found")

            user.verify()
            await uow.user_command.save(user)

            await uow.email_verification_token_command.delete(verification_token.id)
