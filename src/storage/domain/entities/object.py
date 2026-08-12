from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass


@dataclass
class Object:
    key: ObjectKey
    content_type: str
    storage_class: StorageClass
    size: int
    etag: Etag
    versions: list[dict] = field(default_factory=list)
    is_deleted: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        key: ObjectKey,
        storage_class: StorageClass,
        content_type: str = "application/octet-stream",
        size: int = 0,
        etag: Optional[Etag] = None,
    ) -> "Object":
        now = datetime.now(timezone.utc)
        return cls(
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