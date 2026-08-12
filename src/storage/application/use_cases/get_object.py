from dataclasses import dataclass

from src.storage.application.dtos.object_output_dto import ObjectOutputDto
from src.storage.domain.exceptions import ObjectNotFoundError
from src.storage.domain.ports.unit_of_work import StorageUnitOfWork
from src.storage.domain.value_objects.object_key import ObjectKey


@dataclass
class GetObjectUseCase:
    uow: StorageUnitOfWork

    async def execute(self, key: str) -> ObjectOutputDto:
        async with self.uow as uow:
            object_key = ObjectKey(key)

            obj = await uow.objects.query.find_by_key(object_key)
            if obj is None:
                raise ObjectNotFoundError(f"Object '{key}' not found")

            return ObjectOutputDto(
                key=obj.key._value,
                content_type=obj.content_type,
                storage_class=obj.storage_class.name,
                size=obj.size,
                etag=obj.etag._name,
                is_deleted=obj.is_deleted,
                created_at=obj.created_at,
                updated_at=obj.updated_at,
            )