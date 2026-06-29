from dataclasses import dataclass
from datetime import datetime, timedelta

from src.identity.application.dtos.auth_result_dto import AuthResultDto
from src.identity.application.dtos.signup_dto import SignupInputDto
from src.identity.application.use_cases.constants import REFRESH_TOKEN_TTL_DAYS
from src.identity.domain.entities.refresh_token import RefreshToken
from src.identity.domain.entities.user import User
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.token_service import TokenService
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork
from src.identity.domain.value_objects.email import Email


@dataclass
class SignupUseCase:
    uow: IdentityUnitOfWork
    password_hasher: PasswordHasher
    token_service: TokenService

    async def execute(self, dto: SignupInputDto) -> AuthResultDto:
        async with self.uow as uow:
            email = Email(dto.email)

            if await uow.user_query.exists_by_email(email):
                raise ValueError("Email is already registered")

            if await uow.user_query.exists_by_username(dto.username):
                raise ValueError("Username is already taken")

            user = User.create(
                email=email,
                username=dto.username,
                password_hash=self.password_hasher.hash(dto.password),
            )
            await uow.user_command.save(user)

            raw_refresh_token = self.token_service.generate_refresh_token()
            refresh_token = RefreshToken.create(
                user_id=user.id.value,
                token_hash=self.password_hasher.hash(raw_refresh_token),
                expires_at=datetime.now() + timedelta(days=REFRESH_TOKEN_TTL_DAYS),
            )
            await uow.refresh_token_command.save(refresh_token)

            access_token = self.token_service.generate_access_token(user.id.value)

            return AuthResultDto(
                access_token=access_token,
                refresh_token=raw_refresh_token,
                user_id=user.id.value,
                username=user.username,
                email=user.email.address,
            )
