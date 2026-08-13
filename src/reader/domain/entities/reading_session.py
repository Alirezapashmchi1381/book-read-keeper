from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.reader.domain.value_objects.device_id import DeviceId
from src.reader.domain.value_objects.locator import Locator
from src.reader.domain.value_objects.progress_percent import ProgressPercent


@dataclass
class ReadingSession:
    """Aggregate root for a user's reading session on a book.

    Tracks the last known reading position (locator), progress percentage,
    and which device last wrote. Conflict rule: last-write-wins by updated_at.
    """
    id: UUID
    user_id: UUID
    book_id: UUID
    locator: Locator
    progress_percent: ProgressPercent
    device_id: DeviceId | None = None
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def start(
        cls,
        user_id: UUID,
        book_id: UUID,
        locator: Locator,
        progress_percent: ProgressPercent | None = None,
        device_id: DeviceId | None = None,
    ) -> "ReadingSession":
        """Create a new reading session for a (user, book) pair."""
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid4(),
            user_id=user_id,
            book_id=book_id,
            locator=locator,
            progress_percent=progress_percent or ProgressPercent(0.0),
            device_id=device_id,
            started_at=now,
            updated_at=now,
        )

    def update_position(
        self,
        locator: Locator,
        progress_percent: ProgressPercent | None = None,
        device_id: DeviceId | None = None,
    ) -> None:
        """Move the reading position. Last-write-wins by updated_at for v1."""
        if locator.book_id != self.book_id:
            raise ValueError(
                f"Locator book_id {locator.book_id} does not match session book_id {self.book_id}"
            )
        self.locator = locator
        if progress_percent is not None:
            self.progress_percent = progress_percent
        if device_id is not None:
            self.device_id = device_id
        self.updated_at = datetime.now(timezone.utc)

    def is_at(self, locator: Locator) -> bool:
        """Check if the session is at the given locator."""
        return (
            self.locator.book_id == locator.book_id
            and self.locator.value == locator.value
            and self.locator.provider == locator.provider
        )