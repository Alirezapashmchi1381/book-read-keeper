from src.storage.domain.entities.object import Object
from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass
from src.storage.infrastructure.sql.models.object_model import ObjectModel


class ObjectTransformer:
    @staticmethod
    def to_domain(model: ObjectModel) -> Object:
        return Object(
            key=ObjectKey(model.key),
            content_type=model.content_type,
            storage_class=StorageClass(model.storage_class),
            size=model.size,
            etag=Etag(model.etag),
            versions=[],
            is_deleted=model.is_deleted,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Object) -> ObjectModel:
        return ObjectModel(
            key=entity.key._value,
            content_type=entity.content_type,
            storage_class=entity.storage_class.name,
            size=entity.size,
            etag=entity.etag._name,
            is_deleted=entity.is_deleted,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )