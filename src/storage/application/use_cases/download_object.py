from dataclasses import dataclass

from src.storage.application.dtos.object_output_dto import DownloadObjectOutputDto
from src.storage.domain.exceptions import ObjectNotFoundError
from src.storage.domain.ports.file_storage_service import FileStorageService
from src.storage.domain.ports.unit_of_work import StorageUnitOfWork
from src.storage.domain.value_objects.object_key import ObjectKey


@dataclass
class DownloadObjectUseCase:
    uow: StorageUnitOfWork
    file_storage: FileStorageService

    async def execute(self, key: str) -> DownloadObjectOutputDto:
        async with self.uow as uow:
            object_key = ObjectKey(key)

            obj = await uow.objects.query.find_by_key(object_key)
            if obj is None:
                raise ObjectNotFoundError(f"Object '{key}' not found")

            content = await self.file_storage.download(object_key)

            return DownloadObjectOutputDto(
                content=content,
                content_type=obj.content_type,
                etag=obj.etag._name,
            )