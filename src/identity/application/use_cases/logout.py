from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from src.identity.application.dtos.logout_dto import LogoutInputDto
from src.identity.domain.ports.password_hasher import PasswordHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork


@dataclass
class LogoutUseCase:
    uow_factory: Callable[[], IdentityUnitOfWork]
    password_hasher: PasswordHasher

    async def execute(self, dto: LogoutInputDto) -> None:
        async with self.uow_factory() as uow:
            token_hash = self.password_hasher.hash(dto.refresh_token)
            token = await uow.refresh_token_query.find_by_token_hash(token_hash)

            if token is None or not token.is_valid(datetime.now()):
                return

            token.revoke()
            await uow.refresh_token_command.revoke(token.id)
