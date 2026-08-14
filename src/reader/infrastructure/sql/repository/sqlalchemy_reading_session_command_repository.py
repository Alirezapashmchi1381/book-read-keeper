from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.reader.domain.entities.reading_session import ReadingSession
from src.reader.infrastructure.sql.models.reading_session_model import ReadingSessionModel
from src.reader.infrastructure.sql.transformers.reading_session_transformer import ReadingSessionTransformer


class SQLAlchemyReadingSessionCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, session: ReadingSession) -> None:
        model = ReadingSessionTransformer.to_model(session)
        await self._session.merge(model)

    async def delete(self, session_id: UUID) -> None:
        await self._session.execute(
            delete(ReadingSessionModel).where(ReadingSessionModel.id == session_id)
        )