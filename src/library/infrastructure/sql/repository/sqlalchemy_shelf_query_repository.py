from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.library.domain.entities.shelf import Shelf
from src.library.infrastructure.sql.models.shelf_model import ShelfModel
from src.library.infrastructure.sql.models.shelf_book_association import ShelfBookAssociation
from src.library.infrastructure.sql.transformers.shelf_transformer import ShelfTransformer


class SQLAlchemyShelfQueryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, shelf_id: UUID) -> Shelf | None:
        result = await self._session.execute(
            select(ShelfModel).where(ShelfModel.id == shelf_id)
        )
        model = result.scalar_one_or_none()
        return ShelfTransformer.to_domain(model) if model else None

    async def list_all(self) -> list[Shelf]:
        result = await self._session.execute(select(ShelfModel))
        return [ShelfTransformer.to_domain(model) for model in result.scalars().all()]

    async def find_starred(self) -> list[Shelf]:
        result = await self._session.execute(
            select(ShelfModel).where(ShelfModel.is_starred == True)
        )
        return [ShelfTransformer.to_domain(model) for model in result.scalars().all()]

    async def find_shelves_by_book_id(self, book_id: UUID) -> list[Shelf]:
        result = await self._session.execute(
            select(ShelfModel)
            .join(ShelfBookAssociation, ShelfModel.id == ShelfBookAssociation.shelf_id)
            .where(ShelfBookAssociation.book_id == book_id)
        )
        return [ShelfTransformer.to_domain(model) for model in result.scalars().all()]