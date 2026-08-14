from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.reader.infrastructure.sql.models.base import Base


class ReadingSessionModel(Base):
    __tablename__ = "reading_sessions"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False, index=True)
    book_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False, index=True)

    # locator (flattened)
    locator_value: Mapped[str] = mapped_column(String(1024), nullable=False)
    locator_provider: Mapped[str] = mapped_column(String(20), nullable=False)
    locator_sort_key: Mapped[str] = mapped_column(String(200), nullable=False)
    locator_chapter_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    locator_chapter_title: Mapped[str | None] = mapped_column(String(500), nullable=True)

    progress_percent: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    device_id: Mapped[str | None] = mapped_column(String(200), nullable=True)

    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)