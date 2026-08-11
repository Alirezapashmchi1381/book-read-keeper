from typing import Protocol

from src.storage.domain.entities.object import Object
from src.storage.domain.value_objects.bucket_id import BucketID
from src.storage.domain.value_objects.object_key import ObjectKey


class ObjectCommandRepository(Protocol):
    async def save(self, object: Object) -> None: ...

    async def delete(self, bucket_id: BucketID, key: ObjectKey) -> None: ...