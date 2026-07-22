from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.library.domain.entities.book import Book
from src.library.infrastructure.sql.models.book_model import BookModel
from src.library.infrastructure.sql.transformers.book_transformer import BookTransformer


class SQLAlchemyBookQueryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, book_id: UUID) -> Book | None:
        result = await self._session.execute(
            select(BookModel).where(BookModel.id == book_id)
        )
        model = result.scalar_one_or_none()
        return BookTransformer.to_domain(model) if model else None

    async def find_by_ids(self, book_ids: list[UUID]) -> list[Book]:
        result = await self._session.execute(
            select(BookModel).where(BookModel.id.in_(book_ids))
        )
        return [BookTransformer.to_domain(model) for model in result.scalars().all()]

    async def search_by_title(self, title: str) -> list[Book]:
        result = await self._session.execute(
            select(BookModel).where(BookModel.title.ilike(f"%{title}%"))
        )
        return [BookTransformer.to_domain(model) for model in result.scalars().all()]