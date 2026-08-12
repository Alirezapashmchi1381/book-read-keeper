from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ObjectOutputDto:
    key: str
    content_type: str
    storage_class: str
    size: int
    etag: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class DownloadObjectOutputDto:
    content: bytes
    content_type: str
    etag: str