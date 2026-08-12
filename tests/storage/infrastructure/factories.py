from src.storage.domain.entities.object import Object
from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass


def make_object(
    *,
    key: str = "books/1/file.epub",
    content_type: str = "application/epub+zip",
    storage_class: str = "STANDARD",
    size: int = 1024,
    etag: str = "abc123",
    is_deleted: bool = False,
) -> Object:
    return Object.create(
        key=ObjectKey(key),
        storage_class=StorageClass(storage_class),
        content_type=content_type,
        size=size,
        etag=Etag(etag),
    ) if not is_deleted else Object(
        key=ObjectKey(key),
        content_type=content_type,
        storage_class=StorageClass(storage_class),
        size=size,
        etag=Etag(etag),
        is_deleted=is_deleted,
    )