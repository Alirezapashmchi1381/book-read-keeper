from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.domain.entities.object import Object
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.infrastructure.sql.models.object_model import ObjectModel
from src.storage.infrastructure.sql.transformers.object_transformer import ObjectTransformer


class SQLAlchemyObjectCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, object: Object) -> None:
        model = ObjectTransformer.to_model(object)
        await self._session.merge(model)

    async def delete(self, key: ObjectKey) -> None:
        await self._session.execute(
            delete(ObjectModel).where(ObjectModel.key == key._value)
        )