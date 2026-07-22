from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime

from src.library.domain.value_objects.book_metadata import BookMetadata
from src.library.domain.value_objects.book_file import BookFile
from src.library.domain.value_objects.cover import Cover


@dataclass
class Book:
    id: UUID
    metadata: BookMetadata
    book_file: BookFile | None = None
    cover: Cover | None = None
    is_starred: bool = False
    is_deleted: bool = False
    deleted_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, metadata: BookMetadata) -> "Book":
        return cls(
            id=uuid4(),
            metadata=metadata,
        )

    def mark_as_starred(self) -> None:
        self.is_starred = True
        self.updated_at = datetime.now()

    def unstar(self) -> None:
        self.is_starred = False
        self.updated_at = datetime.now()

    def toggle_star(self) -> None:
        self.is_starred = not self.is_starred
        self.updated_at = datetime.now()

    def update_metadata(self, metadata: BookMetadata) -> None:
        self.metadata = metadata
        self.updated_at = datetime.now()

    def update_title(self, title: str) -> None:
        self.metadata = BookMetadata(
            author=self.metadata.author,
            isbn=self.metadata.isbn,
            title=title,
            language=self.metadata.language,
            color=self.metadata.color,
            description=self.metadata.description,
        )
        self.updated_at = datetime.now()

    def attach_book_file(self, book_file: BookFile) -> None:
        self.book_file = book_file
        self.updated_at = datetime.now()

    def attach_cover(self, cover: Cover) -> None:
        self.cover = cover
        self.updated_at = datetime.now()

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()

    def restore(self) -> None:
        self.is_deleted = False
        self.deleted_at = None
        self.updated_at = datetime.now()