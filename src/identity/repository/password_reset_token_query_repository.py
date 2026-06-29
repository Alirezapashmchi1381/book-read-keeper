from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.entities.password_reset_token import PasswordResetToken
from src.identity.repository.models.password_reset_token_model import PasswordResetTokenModel
from src.identity.repository.transformers.password_reset_token_transformer import PasswordResetTokenTransformer


class SQLAlchemyPasswordResetTokenQueryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_token_hash(self, token_hash: str) -> Optional[PasswordResetToken]:
        result = await self._session.execute(
            select(PasswordResetTokenModel).where(PasswordResetTokenModel.token_hash == token_hash)
        )
        model = result.scalar_one_or_none()
        return PasswordResetTokenTransformer.to_domain(model) if model else None
