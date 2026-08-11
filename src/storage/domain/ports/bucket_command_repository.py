from typing import Protocol

from src.storage.domain.entities.bucket import Bucket
from src.storage.domain.value_objects.bucket_id import BucketID


class BucketCommandRepository(Protocol):
    async def save(self, bucket: Bucket) -> None: ...

    async def delete(self, bucket_id: BucketID) -> None: ...