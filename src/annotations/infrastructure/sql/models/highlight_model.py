from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.annotations.infrastructure.sql.models.base import Base


class HighlightModel(Base):
    __tablename__ = "highlights"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False)
    book_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False)

    selected_text: Mapped[str] = mapped_column(String(2000), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    note: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    # start locator
    start_value: Mapped[str] = mapped_column(String(1024), nullable=False)
    start_provider: Mapped[str] = mapped_column(String(20), nullable=False)
    start_sort_key: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    start_chapter_number: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    start_chapter_title: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # end locator
    end_value: Mapped[str] = mapped_column(String(1024), nullable=False)
    end_provider: Mapped[str] = mapped_column(String(20), nullable=False)
    end_sort_key: Mapped[str] = mapped_column(String(200), nullable=False)
    end_chapter_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    end_chapter_title: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)