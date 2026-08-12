from dataclasses import dataclass

from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass


@dataclass(frozen=True)
class UploadObjectInputDto:
    key: str
    content: bytes
    content_type: str = "application/octet-stream"
    storage_class: str = "STANDARD"

    def to_object_key(self) -> ObjectKey:
        return ObjectKey(self.key)

    def to_storage_class(self) -> StorageClass:
        return StorageClass(self.storage_class)