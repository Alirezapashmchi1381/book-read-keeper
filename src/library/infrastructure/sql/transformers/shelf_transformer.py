from uuid import UUID

from src.library.domain.entities.shelf import Shelf
from src.library.domain.value_objects.color import Color
from src.library.domain.value_objects.shelf_name import ShelfName
from src.library.infrastructure.sql.models.shelf_model import ShelfModel


class ShelfTransformer:
    @staticmethod
    def to_domain(model: ShelfModel) -> Shelf:
        return Shelf(
            id=model.id,
            name=ShelfName(model.name),
            color=Color(model.color),
            is_starred=model.is_starred,
            is_deleted=model.is_deleted,
            deleted_at=model.deleted_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Shelf) -> ShelfModel:
        return ShelfModel(
            id=entity.id,
            name=entity.name.name,
            color=entity.color.hex_value,
            is_starred=entity.is_starred,
            is_deleted=entity.is_deleted,
            deleted_at=entity.deleted_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )