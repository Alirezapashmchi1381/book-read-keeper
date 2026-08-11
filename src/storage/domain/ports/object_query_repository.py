from typing import Protocol

from src.storage.domain.entities.object import Object
from src.storage.domain.value_objects.bucket_id import BucketID
from src.storage.domain.value_objects.object_key import ObjectKey


class ObjectQueryRepository(Protocol):
    async def find_by_key(self, bucket_id: BucketID, key: ObjectKey) -> Object | None: ...

    async def find_by_bucket(self, bucket_id: BucketID) -> list[Object]: ...

    async def search_by_prefix(self, bucket_id: BucketID, prefix: str) -> list[Object]: ...