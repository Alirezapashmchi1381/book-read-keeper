from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.entities.email_verification_token import EmailVerificationToken
from identity.infrastructure.repository.models.email_verification_token_model import EmailVerificationTokenModel
from identity.infrastructure.repository.transformers.email_verification_token_transformer import EmailVerificationTokenTransformer


class SQLAlchemyEmailVerificationTokenQueryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_token_hash(self, token_hash: str) -> Optional[EmailVerificationToken]:
        result = await self._session.execute(
            select(EmailVerificationTokenModel).where(EmailVerificationTokenModel.token_hash == token_hash)
        )
        model = result.scalar_one_or_none()
        return EmailVerificationTokenTransformer.to_domain(model) if model else None
