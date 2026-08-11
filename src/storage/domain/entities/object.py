from dataclasses import dataclass
from datetime import datetime
from typing import Optional,List
from src.storage.domain.value_objects.bucket_id import BucketID
from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass




@dataclass
class Object:
    bucket_id : BucketID
    key : Object
    content_type: str
    storage_class: StorageClass
    size : int
    etag: Etag
    version: List[dict]
    is_deleted: bool
    created_at: datetime
    updated_at : datetime

    @classmethod
    def create(
        cls,
        bucket_id: BucketID,
        key: ObjectKey,
        storage_class: StorageClass,
        content_type: str = "application/octet-stream",
        size: int = 0,
        etag: Optional[Etag] = None,
    ) -> "Object":
        now = datetime.utcnow()
        return cls(
            bucket_id=bucket_id,
            key=key,
            content_type=content_type,
            storage_class=storage_class,
            size=size,
            etag=etag or Etag(""),   
            versions=[],             
            created_at=now,
            updated_at=now,
            is_deleted=False,
        )
