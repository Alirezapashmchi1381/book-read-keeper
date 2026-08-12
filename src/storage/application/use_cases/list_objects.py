from dataclasses import dataclass

from src.storage.application.dtos.object_output_dto import ObjectOutputDto
from src.storage.domain.ports.unit_of_work import StorageUnitOfWork


@dataclass
class ListObjectsUseCase:
    uow: StorageUnitOfWork

    async def execute(self) -> list[ObjectOutputDto]:
        async with self.uow as uow:
            objects = await uow.objects.query.list_all()
            return [
                ObjectOutputDto(
                    key=obj.key._value,
                    content_type=obj.content_type,
                    storage_class=obj.storage_class.name,
                    size=obj.size,
                    etag=obj.etag._name,
                    is_deleted=obj.is_deleted,
                    created_at=obj.created_at,
                    updated_at=obj.updated_at,
                )
                for obj in objects
            ]