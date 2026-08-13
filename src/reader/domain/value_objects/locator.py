from dataclasses import dataclass
from uuid import UUID

from src.reader.domain.exceptions import InvalidLocatorError


@dataclass(frozen=True)
class Locator:
    """Decoupled, chapter-aware reading position."""
    book_id: UUID
    value: str
    provider: str
    sort_key: str
    chapter_number: int | None = None
    chapter_title: str | None = None

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidLocatorError("Locator value cannot be empty")
        if not self.provider.strip():
            raise InvalidLocatorError("Locator provider cannot be empty")
        if not self.sort_key.strip():
            raise InvalidLocatorError("Locator sort_key cannot be empty")