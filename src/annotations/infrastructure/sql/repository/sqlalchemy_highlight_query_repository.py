from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.annotations.domain.entities.highlight import Highlight
from src.annotations.infrastructure.sql.models.highlight_model import HighlightModel
from src.annotations.infrastructure.sql.transformers.highlight_transformer import HighlightTransformer


class SQLAlchemyHighlightQueryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, highlight_id: UUID) -> Highlight | None:
        result = await self._session.execute(
            select(HighlightModel).where(HighlightModel.id == highlight_id)
        )
        model = result.scalar_one_or_none()
        return HighlightTransformer.to_domain(model) if model else None

    async def find_by_book(
        self,
        user_id: UUID,
        book_id: UUID,
        chapter: int | None = None,
    ) -> list[Highlight]:
        conditions = [
            HighlightModel.user_id == user_id,
            HighlightModel.book_id == book_id,
        ]
        if chapter is not None:
            conditions.append(HighlightModel.start_chapter_number == chapter)
        result = await self._session.execute(
            select(HighlightModel)
            .where(and_(*conditions))
            .order_by(HighlightModel.start_sort_key)
        )
        return [HighlightTransformer.to_domain(model) for model in result.scalars().all()]

    async def list_by_user(self, user_id: UUID) -> list[Highlight]:
        result = await self._session.execute(
            select(HighlightModel)
            .where(HighlightModel.user_id == user_id)
            .order_by(HighlightModel.start_sort_key)
        )
        return [HighlightTransformer.to_domain(model) for model in result.scalars().all()]