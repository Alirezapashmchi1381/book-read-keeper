from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class LocatorOutputDto:
    book_id: UUID
    chapter_number: int | None
    chapter_title: str | None
    value: str
    provider: str
    sort_key: str


@dataclass(frozen=True)
class HighlightOutputDto:
    id: UUID
    selected_text: str
    color: str
    note: str | None
    locator: LocatorOutputDto
    end_locator: LocatorOutputDto
    is_deleted: bool
    created_at: datetime
    updated_at: datetime