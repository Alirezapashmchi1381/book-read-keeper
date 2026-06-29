from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.entities.refresh_token import RefreshToken
from src.identity.repository.models.refresh_token_model import RefreshTokenModel
from src.identity.repository.transformers.refresh_token_transformer import RefreshTokenTransformer


class SQLAlchemyRefreshTokenQueryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, token_id: UUID) -> Optional[RefreshToken]:
        result = await self._session.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.id == token_id)
        )
        model = result.scalar_one_or_none()
        return RefreshTokenTransformer.to_domain(model) if model else None

    async def find_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        result = await self._session.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
        )
        model = result.scalar_one_or_none()
        return RefreshTokenTransformer.to_domain(model) if model else None

    async def find_all_by_user_id(self, user_id: UUID) -> list[RefreshToken]:
        result = await self._session.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id)
        )
        return [RefreshTokenTransformer.to_domain(m) for m in result.scalars().all()]
