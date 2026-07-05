from dataclasses import dataclass
from datetime import datetime, timedelta

from src.identity.application.dtos.request_password_reset_dto import RequestPasswordResetInputDto
from src.identity.application.use_cases.constants import RESET_TOKEN_TTL_HOURS
from src.identity.domain.entities.password_reset_token import PasswordResetToken
from src.identity.domain.ports.email_service import EmailService
from src.identity.domain.ports.secret_generator import SecretGenerator
from src.identity.domain.ports.token_hasher import TokenHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.email import Email


@dataclass
class RequestPasswordResetUseCase:
    uow: IdentityUnitOfWork
    token_hasher: TokenHasher
    secret_generator: SecretGenerator
    email_service: EmailService

    async def execute(self, dto: RequestPasswordResetInputDto) -> None:
        async with self.uow as uow:
            email = Email(dto.email)
            user = await uow.users.query.find_by_email(email)

            # Silent no-op: avoids leaking whether an email is registered
            if user is None:
                return

            # Invalidate any existing reset tokens before issuing a new one
            await uow.password_reset_tokens.command.delete_all_for_user(user.id)

            raw_token = self.secret_generator.generate()
            reset_token = PasswordResetToken.create(
                user_id=user.id,
                token_hash=self.token_hasher.hash(raw_token),
                expires_at=datetime.now() + timedelta(hours=RESET_TOKEN_TTL_HOURS),
            )
            await uow.password_reset_tokens.command.save(reset_token)

        await self.email_service.send_password_reset(user.email.address, raw_token)
