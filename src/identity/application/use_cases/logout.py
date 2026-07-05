from dataclasses import dataclass
from datetime import datetime

from src.identity.application.dtos.logout_dto import LogoutInputDto
from src.identity.domain.ports.token_hasher import TokenHasher
from src.identity.domain.ports.unit_of_work import IdentityUnitOfWork


@dataclass
class LogoutUseCase:
    uow: IdentityUnitOfWork
    token_hasher: TokenHasher

    async def execute(self, dto: LogoutInputDto) -> None:
        async with self.uow as uow:
            token_hash = self.token_hasher.hash(dto.refresh_token)
            token = await uow.refresh_tokens.query.find_by_token_hash(token_hash)

            if token is None or not token.is_valid(datetime.now()):
                return

            token.revoke()
            await uow.refresh_tokens.command.revoke(token.id)
