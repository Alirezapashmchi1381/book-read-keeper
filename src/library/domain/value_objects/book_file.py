from dataclasses import dataclass

from src.library.domain.value_objects.storage_key import StorageKey
from src.library.domain.value_objects.checksum import Checksum
from src.library.domain.value_objects.file_format import FileFormat
from src.library.domain.value_objects.file_size import FileSize
from src.library.domain.value_objects.mime_type import MimeType


@dataclass
class BookFile:
    storage_key: StorageKey
    format: FileFormat
    checksum: Checksum
    size: FileSize
    mime_type: MimeType