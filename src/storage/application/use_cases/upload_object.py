from dataclasses import dataclass

from src.storage.application.dtos.upload_object_dto import UploadObjectInputDto
from src.storage.domain.entities.object import Object
from src.storage.domain.ports.file_storage_service import FileStorageService
from src.storage.domain.ports.unit_of_work import StorageUnitOfWork


@dataclass
class UploadObjectUseCase:
    uow: StorageUnitOfWork
    file_storage: FileStorageService

    async def execute(self, dto: UploadObjectInputDto) -> Object:
        async with self.uow as uow:
            key = dto.to_object_key()
            storage_class = dto.to_storage_class()

            etag = await self.file_storage.upload(
                key=key,
                content=dto.content,
                content_type=dto.content_type,
                storage_class=storage_class,
            )

            obj = Object.create(
                key=key,
                storage_class=storage_class,
                content_type=dto.content_type,
                size=len(dto.content),
                etag=etag,
            )

            await uow.objects.command.save(obj)
            await uow.commit()
            return obj