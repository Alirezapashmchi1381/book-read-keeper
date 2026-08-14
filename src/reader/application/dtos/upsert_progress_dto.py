from dataclasses import dataclass
from uuid import UUID

from src.reader.domain.value_objects.device_id import DeviceId
from src.reader.domain.value_objects.locator import Locator
from src.reader.domain.value_objects.progress_percent import ProgressPercent


@dataclass(frozen=True)
class UpsertProgressInputDto:
    user_id: UUID
    book_id: UUID
    locator_value: str
    locator_provider: str
    locator_sort_key: str
    locator_chapter_number: int | None = None
    locator_chapter_title: str | None = None
    progress_percent: float | None = None
    device_id: str | None = None

    def to_locator(self) -> Locator:
        return Locator(
            book_id=self.book_id,
            value=self.locator_value,
            provider=self.locator_provider,
            sort_key=self.locator_sort_key,
            chapter_number=self.locator_chapter_number,
            chapter_title=self.locator_chapter_title,
        )

    def to_progress(self) -> ProgressPercent | None:
        if self.progress_percent is None:
            return None
        return ProgressPercent(self.progress_percent)

    def to_device_id(self) -> DeviceId | None:
        if self.device_id is None:
            return None
        return DeviceId(self.device_id)