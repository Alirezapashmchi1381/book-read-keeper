from dataclasses import dataclass
from uuid import UUID

from src.library.domain.ports.file_storage_service import FileStorageService
from src.library.domain.value_objects.book_file import BookFile
from src.library.domain.value_objects.checksum import Checksum
from src.library.domain.value_objects.cover import Cover
from src.library.domain.value_objects.file_format import FileFormat
from src.library.domain.value_objects.file_size import FileSize
from src.library.domain.value_objects.mime_type import MimeType
from src.library.domain.value_objects.storage_key import StorageKey
from src.storage.application.dtos.upload_object_dto import UploadObjectInputDto
from src.storage.application.use_cases.delete_object import DeleteObjectUseCase
from src.storage.application.use_cases.download_object import DownloadObjectUseCase
from src.storage.application.use_cases.upload_object import UploadObjectUseCase
from src.storage.domain.ports.file_storage_service import FileStorageService as StorageFileStoragePort


@dataclass
class StorageFileStorageService(FileStorageService):
    """Library file storage backed by the storage module's use cases."""

    upload: UploadObjectUseCase
    download: DownloadObjectUseCase
    delete: DeleteObjectUseCase
    storage_file_storage: StorageFileStoragePort

    async def store_book_file(
        self,
        book_id: UUID,
        content: bytes,
        format: FileFormat,
    ) -> BookFile:
        key = f"books/{book_id}/file"
        obj = await self.upload.execute(
            UploadObjectInputDto(
                key=key,
                content=content,
                content_type=f"application/{format.value}",
            )
        )
        return BookFile(
            storage_key=StorageKey(key),
            format=format,
            checksum=Checksum(algorithm="md5", value=obj.etag._name),
            size=FileSize(len(content) or 1),  # ensure positive for empty content
            mime_type=MimeType(f"application/{format.value}"),
        )

    async def store_cover(
        self,
        book_id: UUID,
        content: bytes,
        mime_type: MimeType,
    ) -> Cover:
        key = f"books/{book_id}/cover"
        await self.upload.execute(
            UploadObjectInputDto(
                key=key,
                content=content,
                content_type=mime_type.value,
            )
        )
        return Cover(
            storage_key=StorageKey(key),
            width=300,
            height=400,
            generated=False,
        )

    async def delete_file(self, storage_key: str) -> None:
        await self.delete.execute(storage_key)

    async def get_download_url(self, storage_key: str) -> str:
        from src.storage.domain.value_objects.object_key import ObjectKey

        return await self.storage_file_storage.get_presigned_url(ObjectKey(storage_key))