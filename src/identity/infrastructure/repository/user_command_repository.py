from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.entities.user import User
from src.identity.domain.value_objects.user_id import UserId
from identity.infrastructure.repository.models.user_model import UserModel
from identity.infrastructure.repository.transformers.user_transformer import UserTransformer


class SQLAlchemyUserCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> None:
        model = UserTransformer.to_model(user)
        await self._session.merge(model)

    async def delete(self, user_id: UserId) -> None:
        await self._session.execute(
            delete(UserModel).where(UserModel.id == user_id.value)
        )
