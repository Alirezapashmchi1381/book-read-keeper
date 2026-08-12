from dataclasses import dataclass

from src.storage.domain.exceptions import ObjectNotFoundError
from src.storage.domain.ports.file_storage_service import FileStorageService
from src.storage.domain.ports.unit_of_work import StorageUnitOfWork
from src.storage.domain.value_objects.object_key import ObjectKey


@dataclass
class DeleteObjectUseCase:
    uow: StorageUnitOfWork
    file_storage: FileStorageService

    async def execute(self, key: str) -> None:
        async with self.uow as uow:
            object_key = ObjectKey(key)

            obj = await uow.objects.query.find_by_key(object_key)
            if obj is None:
                raise ObjectNotFoundError(f"Object '{key}' not found")

            await self.file_storage.delete(object_key)
            await uow.objects.command.delete(object_key)
            await uow.commit()