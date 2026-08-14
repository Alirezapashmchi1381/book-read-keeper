from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class SessionOutputDto:
    id: UUID
    user_id: UUID
    book_id: UUID
    locator_value: str
    locator_provider: str
    locator_sort_key: str
    locator_chapter_number: int | None
    locator_chapter_title: str | None
    progress_percent: float
    device_id: str | None
    started_at: datetime
    updated_at: datetime