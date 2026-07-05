from dataclasses import dataclass
from datetime import datetime, timedelta

from src.identity.application.dtos.auth_result_dto import AuthResultDto
from src.identity.application.dtos.login_dto import LoginInputDto
from src.identity.application.use_cases.constants import REFRESH_TOKEN_TTL_DAYS
from src.identity.domain.entities.refresh_token import RefreshToken
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.secret_generator import SecretGenerator
from src.identity.domain.ports.token_hasher import TokenHasher
from src.identity.domain.ports.token_service import TokenService
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.email import Email


@dataclass
class LoginUseCase:
    uow: IdentityUnitOfWork
    password_hasher: PasswordHasher
    token_hasher: TokenHasher
    token_service: TokenService
    secret_generator: SecretGenerator

    async def execute(self, dto: LoginInputDto) -> AuthResultDto:
        async with self.uow as uow:
            email = Email(dto.email)
            user = await uow.users.query.find_by_email(email)

            # Single generic message to avoid leaking whether the email exists.
            if user is None or not user.verify_password(dto.password, self.password_hasher):
                raise ValueError("Invalid credentials")

            if not user.is_active:
                raise ValueError("Account is deactivated")

            await uow.refresh_tokens.command.revoke_all_for_user(user.id)

            raw_refresh_token = self.secret_generator.generate()
            refresh_token = RefreshToken.create(
                user_id=user.id,
                token_hash=self.token_hasher.hash(raw_refresh_token),
                expires_at=datetime.now() + timedelta(days=REFRESH_TOKEN_TTL_DAYS),
            )
            await uow.refresh_tokens.command.save(refresh_token)

            access_token = self.token_service.generate_access_token(user.id)

            return AuthResultDto(
                access_token=access_token,
                refresh_token=raw_refresh_token,
                user_id=user.id,
                username=user.username,
                email=user.email.address,
            )
