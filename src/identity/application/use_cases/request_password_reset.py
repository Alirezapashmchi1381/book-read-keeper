from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable

from src.identity.application.dtos.request_password_reset_dto import RequestPasswordResetInputDto
from src.identity.application.use_cases.constants import RESET_TOKEN_TTL_HOURS
from src.identity.domain.entities.password_reset_token import PasswordResetToken
from src.identity.domain.ports.email_service import EmailService
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.token_service import TokenService
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.email import Email


@dataclass
class RequestPasswordResetUseCase:
    uow_factory: Callable[[], IdentityUnitOfWork]
    password_hasher: PasswordHasher
    token_service: TokenService
    email_service: EmailService

    async def execute(self, dto: RequestPasswordResetInputDto) -> None:
        async with self.uow_factory() as uow:
            email = Email(dto.email)
            user = await uow.user_query.find_by_email(email)

            # Silent no-op: avoids leaking whether an email is registered
            if user is None:
                return

            # Invalidate any existing reset tokens before issuing a new one
            await uow.password_reset_token_command.delete_all_for_user(user.id.value)

            raw_token = self.token_service.generate_refresh_token()
            reset_token = PasswordResetToken.create(
                user_id=user.id.value,
                token_hash=self.password_hasher.hash(raw_token),
                expires_at=datetime.now() + timedelta(hours=RESET_TOKEN_TTL_HOURS),
            )
            await uow.password_reset_token_command.save(reset_token)

        await self.email_service.send_password_reset(user.email.address, raw_token)
