from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable

from src.identity.application.dtos.refresh_token_dto import RefreshTokenInputDto, RefreshTokenResultDto
from src.identity.application.use_cases.constants import REFRESH_TOKEN_TTL_DAYS
from src.identity.domain.entities.refresh_token import RefreshToken
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.token_service import TokenService
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork


@dataclass
class RefreshTokenUseCase:
    uow_factory: Callable[[], IdentityUnitOfWork]
    password_hasher: PasswordHasher
    token_service: TokenService

    async def execute(self, dto: RefreshTokenInputDto) -> RefreshTokenResultDto:
        async with self.uow_factory() as uow:
            token_hash = self.password_hasher.hash(dto.refresh_token)
            token = await uow.refresh_token_query.find_by_token_hash(token_hash)

            if token is None or not token.is_valid(datetime.now()):
                raise ValueError("Invalid or expired refresh token")

            # Rotate: revoke old token, issue a new one
            await uow.refresh_token_command.revoke(token.id)

            raw_new_refresh_token = self.token_service.generate_refresh_token()
            new_refresh_token = RefreshToken.create(
                user_id=token.user_id,
                token_hash=self.password_hasher.hash(raw_new_refresh_token),
                expires_at=datetime.now() + timedelta(days=REFRESH_TOKEN_TTL_DAYS),
            )
            await uow.refresh_token_command.save(new_refresh_token)

            access_token = self.token_service.generate_access_token(token.user_id)

            return RefreshTokenResultDto(
                access_token=access_token,
                refresh_token=raw_new_refresh_token,
            )
