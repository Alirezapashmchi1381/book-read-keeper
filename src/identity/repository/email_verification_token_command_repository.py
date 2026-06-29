from datetime import datetime
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.entities.email_verification_token import EmailVerificationToken
from src.identity.repository.models.email_verification_token_model import EmailVerificationTokenModel
from src.identity.repository.transformers.email_verification_token_transformer import EmailVerificationTokenTransformer


class SQLAlchemyEmailVerificationTokenCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, token: EmailVerificationToken) -> None:
        model = EmailVerificationTokenTransformer.to_model(token)
        await self._session.merge(model)

    async def delete(self, token_id: UUID) -> None:
        await self._session.execute(
            delete(EmailVerificationTokenModel).where(EmailVerificationTokenModel.id == token_id)
        )

    async def delete_all_for_user(self, user_id: UUID) -> None:
        await self._session.execute(
            delete(EmailVerificationTokenModel).where(EmailVerificationTokenModel.user_id == user_id)
        )

    async def delete_expired(self) -> None:
        await self._session.execute(
            delete(EmailVerificationTokenModel).where(EmailVerificationTokenModel.expires_at < datetime.now())
        )
