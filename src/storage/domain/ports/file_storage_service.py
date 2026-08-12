from typing import Protocol

from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass


class FileStorageService(Protocol):
    """Port for actual file upload and download operations."""

    async def upload(
        self,
        key: ObjectKey,
        content: bytes,
        content_type: str,
        storage_class: StorageClass,
    ) -> Etag:
        """Upload file content and return the etag (checksum)."""
        ...

    async def download(self, key: ObjectKey) -> bytes:
        """Download file content by key."""
        ...

    async def delete(self, key: ObjectKey) -> None:
        """Delete a file from storage."""
        ...

    async def get_presigned_url(self, key: ObjectKey, expires_in: int = 3600) -> str:
        """Get a presigned URL for direct download."""
        ...