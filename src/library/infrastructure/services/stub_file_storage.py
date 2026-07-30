import hashlib
from uuid import UUID, uuid4

from src.library.domain.ports.file_storage_service import FileStorageService
from src.library.domain.value_objects.book_file import BookFile
from src.library.domain.value_objects.checksum import Checksum
from src.library.domain.value_objects.cover import Cover
from src.library.domain.value_objects.file_format import FileFormat
from src.library.domain.value_objects.file_size import FileSize
from src.library.domain.value_objects.mime_type import MimeType
from src.library.domain.value_objects.storage_key import StorageKey


class StubFileStorageService(FileStorageService):
    """Stub implementation that stores nothing — for development use."""

    async def store_book_file(
        self,
        book_id: UUID,
        content: bytes,
        format: FileFormat,
    ) -> BookFile:
        return BookFile(
            storage_key=StorageKey(f"books/{book_id}/file/{uuid4()}"),
            format=format,
            checksum=Checksum(algorithm="sha256", value=hashlib.sha256(content).hexdigest()),
            size=FileSize(len(content) or 1),  # ensure positive for empty content
            mime_type=MimeType(f"application/{format.value}"),
        )

    async def store_cover(
        self,
        book_id: UUID,
        content: bytes,
        mime_type: MimeType,
    ) -> Cover:
        return Cover(
            storage_key=StorageKey(f"books/{book_id}/cover/{uuid4()}"),
            width=300,
            height=400,
            generated=False,
        )

    async def delete_file(self, storage_key: str) -> None:
        pass

    async def get_download_url(self, storage_key: str) -> str:
        return f"https://storage.example.com/{storage_key}"