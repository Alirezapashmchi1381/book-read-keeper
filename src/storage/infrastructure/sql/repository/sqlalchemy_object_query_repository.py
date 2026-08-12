from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.domain.entities.object import Object
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.infrastructure.sql.models.object_model import ObjectModel
from src.storage.infrastructure.sql.transformers.object_transformer import ObjectTransformer


class SQLAlchemyObjectQueryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_key(self, key: ObjectKey) -> Object | None:
        result = await self._session.execute(
            select(ObjectModel).where(ObjectModel.key == key._value)
        )
        model = result.scalar_one_or_none()
        return ObjectTransformer.to_domain(model) if model else None

    async def list_all(self) -> list[Object]:
        result = await self._session.execute(select(ObjectModel))
        return [ObjectTransformer.to_domain(model) for model in result.scalars().all()]

    async def search_by_prefix(self, prefix: str) -> list[Object]:
        result = await self._session.execute(
            select(ObjectModel).where(ObjectModel.key.like(f"{prefix}%"))
        )
        return [ObjectTransformer.to_domain(model) for model in result.scalars().all()]