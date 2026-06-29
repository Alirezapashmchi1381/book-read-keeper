from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.entities.refresh_token import RefreshToken
from src.identity.repository.models.refresh_token_model import RefreshTokenModel
from src.identity.repository.transformers.refresh_token_transformer import RefreshTokenTransformer


class SQLAlchemyRefreshTokenCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, token: RefreshToken) -> None:
        model = RefreshTokenTransformer.to_model(token)
        await self._session.merge(model)

    async def revoke(self, token_id: UUID) -> None:
        await self._session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == token_id)
            .values(revoked=True)
        )

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        await self._session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == user_id)
            .values(revoked=True)
        )

    async def delete_expired(self) -> None:
        await self._session.execute(
            delete(RefreshTokenModel).where(RefreshTokenModel.expires_at < datetime.now())
        )
