from typing import Protocol

from src.storage.domain.entities.bucket import Bucket
from src.storage.domain.value_objects.bucket_id import BucketID


class BucketQueryRepository(Protocol):
    async def find_by_id(self, bucket_id: BucketID) -> Bucket | None: ...

    async def find_by_owner(self, owner: str) -> list[Bucket]: ...

    async def list_all(self) -> list[Bucket]: ...