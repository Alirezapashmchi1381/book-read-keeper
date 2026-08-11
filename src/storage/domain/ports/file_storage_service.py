from typing import Protocol

from src.storage.domain.value_objects.bucket_id import BucketID
from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass


class FileStorageService(Protocol):
    """Port for actual file upload and download operations."""

    async def upload(
        self,
        bucket_id: BucketID,
        key: ObjectKey,
        content: bytes,
        content_type: str,
        storage_class: StorageClass,
    ) -> Etag:
        """Upload file content and return the etag (checksum)."""
        ...

    async def download(self, bucket_id: BucketID, key: ObjectKey) -> bytes:
        """Download file content by bucket and key."""
        ...

    async def delete(self, bucket_id: BucketID, key: ObjectKey) -> None:
        """Delete a file from storage."""
        ...

    async def get_presigned_url(
        self, bucket_id: BucketID, key: ObjectKey, expires_in: int = 3600
    ) -> str:
        """Get a presigned URL for direct download."""
        ...