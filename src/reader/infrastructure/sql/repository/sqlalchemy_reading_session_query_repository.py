from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.reader.domain.entities.reading_session import ReadingSession
from src.reader.infrastructure.sql.models.reading_session_model import ReadingSessionModel
from src.reader.infrastructure.sql.transformers.reading_session_transformer import ReadingSessionTransformer


class SQLAlchemyReadingSessionQueryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, session_id: UUID) -> ReadingSession | None:
        result = await self._session.execute(
            select(ReadingSessionModel).where(ReadingSessionModel.id == session_id)
        )
        model = result.scalar_one_or_none()
        return ReadingSessionTransformer.to_domain(model) if model else None

    async def find_by_user_and_book(self, user_id: UUID, book_id: UUID) -> ReadingSession | None:
        result = await self._session.execute(
            select(ReadingSessionModel).where(
                and_(
                    ReadingSessionModel.user_id == user_id,
                    ReadingSessionModel.book_id == book_id,
                )
            )
        )
        model = result.scalar_one_or_none()
        return ReadingSessionTransformer.to_domain(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[ReadingSession]:
        result = await self._session.execute(
            select(ReadingSessionModel)
            .where(ReadingSessionModel.user_id == user_id)
            .order_by(ReadingSessionModel.updated_at.desc())
        )
        return [ReadingSessionTransformer.to_domain(m) for m in result.scalars().all()]