from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.library.domain.entities.book import Book
from src.library.infrastructure.sql.models.book_model import BookModel
from src.library.infrastructure.sql.transformers.book_transformer import BookTransformer


class SQLAlchemyBookCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, book: Book) -> None:
        model = BookTransformer.to_model(book)
        await self._session.merge(model)

    async def delete(self, book_id: UUID) -> None:
        await self._session.execute(
            delete(BookModel).where(BookModel.id == book_id)
        )