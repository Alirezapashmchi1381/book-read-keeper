from typing import Protocol
from uuid import UUID

from src.library.domain.value_objects.book_file import BookFile
from src.library.domain.value_objects.cover import Cover
from src.library.domain.value_objects.checksum import Checksum
from src.library.domain.value_objects.file_format import FileFormat
from src.library.domain.value_objects.file_size import FileSize
from src.library.domain.value_objects.mime_type import MimeType


class FileStorageService(Protocol):
    """Port for storing and retrieving book files and covers."""

    async def store_book_file(
        self, book_id: UUID, content: bytes, format: FileFormat
    ) -> BookFile:
        """Store a book file and return the domain BookFile value object."""
        ...

    async def store_cover(
        self, book_id: UUID, content: bytes, mime_type: MimeType
    ) -> Cover:
        """Store a cover image and return the domain Cover value object."""
        ...

    async def delete_file(self, storage_key: str) -> None:
        """Delete a file from storage by its storage key."""
        ...

    async def get_download_url(self, storage_key: str) -> str:
        """Get a downloadable URL for a stored file."""
        ...