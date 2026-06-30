from datetime import datetime
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.entities.password_reset_token import PasswordResetToken
from identity.infrastructure.repository.models.password_reset_token_model import PasswordResetTokenModel
from identity.infrastructure.repository.transformers.password_reset_token_transformer import PasswordResetTokenTransformer


class SQLAlchemyPasswordResetTokenCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, token: PasswordResetToken) -> None:
        model = PasswordResetTokenTransformer.to_model(token)
        await self._session.merge(model)

    async def delete(self, token_id: UUID) -> None:
        await self._session.execute(
            delete(PasswordResetTokenModel).where(PasswordResetTokenModel.id == token_id)
        )

    async def delete_all_for_user(self, user_id: UUID) -> None:
        await self._session.execute(
            delete(PasswordResetTokenModel).where(PasswordResetTokenModel.user_id == user_id)
        )

    async def delete_expired(self) -> None:
        await self._session.execute(
            delete(PasswordResetTokenModel).where(PasswordResetTokenModel.expires_at < datetime.now())
        )
