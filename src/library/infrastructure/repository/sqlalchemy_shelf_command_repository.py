from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.library.domain.entities.shelf import Shelf
from src.library.infrastructure.sql.models.shelf_model import ShelfModel
from src.library.infrastructure.sql.models.shelf_book_association import ShelfBookAssociation as ShelfBookAssociationModel
from src.library.infrastructure.sql.transformers.shelf_transformer import ShelfTransformer


class SQLAlchemyShelfCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, shelf: Shelf) -> None:
        model = ShelfTransformer.to_model(shelf)
        await self._session.merge(model)
        await self._session.flush()

        # Sync the join table: delete old associations, insert new ones
        await self._session.execute(
            delete(ShelfBookAssociationModel).where(
                ShelfBookAssociationModel.shelf_id == shelf.id
            )
        )
        await self._session.flush()

        for association in shelf.book_associations:
            assoc_model = ShelfBookAssociationModel(
                shelf_id=association.shelf_id,
                book_id=association.book_id,
                position=association.position,
            )
            self._session.add(assoc_model)

    async def delete(self, shelf_id: UUID) -> None:
        await self._session.execute(
            delete(ShelfModel).where(ShelfModel.id == shelf_id)
        )