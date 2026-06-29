from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from src.identity.application.dtos.verify_email_dto import RequestEmailVerificationInputDto
from src.identity.application.use_cases.constants import VERIFICATION_TOKEN_TTL_HOURS
from src.identity.domain.entities.email_verification_token import EmailVerificationToken
from src.identity.domain.ports.email_service import EmailService
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.token_service import TokenService
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.user_id import UserId


@dataclass
class RequestEmailVerificationUseCase:
    uow: IdentityUnitOfWork
    password_hasher: PasswordHasher
    token_service: TokenService
    email_service: EmailService

    async def execute(self, dto: RequestEmailVerificationInputDto) -> None:
        async with self.uow as uow:
            user = await uow.user_query.find_by_id(UserId(UUID(dto.user_id)))

            if user is None:
                raise ValueError("User not found")

            if user.is_verified:
                return

            await uow.email_verification_token_command.delete_all_for_user(user.id.value)

            raw_token = self.token_service.generate_refresh_token()
            verification_token = EmailVerificationToken.create(
                user_id=user.id.value,
                token_hash=self.password_hasher.hash(raw_token),
                expires_at=datetime.now() + timedelta(hours=VERIFICATION_TOKEN_TTL_HOURS),
            )
            await uow.email_verification_token_command.save(verification_token)

        await self.email_service.send_email_verification(user.email.address, raw_token)
