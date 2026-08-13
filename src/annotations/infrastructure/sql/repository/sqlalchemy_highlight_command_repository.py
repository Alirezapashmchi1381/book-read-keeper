from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.annotations.domain.entities.highlight import Highlight
from src.annotations.infrastructure.sql.models.highlight_model import HighlightModel
from src.annotations.infrastructure.sql.transformers.highlight_transformer import HighlightTransformer


class SQLAlchemyHighlightCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, highlight: Highlight) -> None:
        model = HighlightTransformer.to_model(highlight)
        await self._session.merge(model)

    async def delete(self, highlight: Highlight) -> None:
        await self._session.execute(
            delete(HighlightModel).where(HighlightModel.id == highlight.id)
        )