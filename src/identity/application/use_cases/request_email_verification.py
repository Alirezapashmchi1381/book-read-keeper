from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from src.identity.application.dtos.verify_email_dto import RequestEmailVerificationInputDto
from src.identity.application.use_cases.constants import VERIFICATION_TOKEN_TTL_HOURS
from src.identity.domain.entities.email_verification_token import EmailVerificationToken
from src.identity.domain.exceptions import NotFoundError
from src.identity.domain.ports.email_service import EmailService
from src.identity.domain.ports.secret_generator import SecretGenerator
from src.identity.domain.ports.token_hasher import TokenHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork


@dataclass
class RequestEmailVerificationUseCase:
    uow: IdentityUnitOfWork
    token_hasher: TokenHasher
    secret_generator: SecretGenerator
    email_service: EmailService

    async def execute(self, dto: RequestEmailVerificationInputDto) -> None:
        async with self.uow as uow:
            user = await uow.users.query.find_by_id(UUID(dto.user_id))

            if user is None:
                raise NotFoundError("User not found")

            if user.is_verified:
                return

            await uow.email_verification_tokens.command.delete_all_for_user(user.id)

            raw_token = self.secret_generator.generate()
            verification_token = EmailVerificationToken.create(
                user_id=user.id,
                token_hash=self.token_hasher.hash(raw_token),
                expires_at=datetime.now() + timedelta(hours=VERIFICATION_TOKEN_TTL_HOURS),
            )
            await uow.email_verification_tokens.command.save(verification_token)

        await self.email_service.send_email_verification(user.email.address, raw_token)
