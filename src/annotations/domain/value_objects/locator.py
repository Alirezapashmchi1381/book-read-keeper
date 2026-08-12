from dataclasses import dataclass
from uuid import UUID

from src.annotations.domain.exceptions import InvalidLocatorError
from src.annotations.domain.value_objects.chapter import Chapter


@dataclass(frozen=True)
class Locator:
    book_id: UUID
    value: str
    provider: str
    sort_key: str
    chapter: Chapter | None = None

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidLocatorError("Locator value cannot be empty")
        if not self.provider.strip():
            raise InvalidLocatorError("Locator provider cannot be empty")
        if not self.sort_key.strip():
            raise InvalidLocatorError("Locator sort_key cannot be empty")