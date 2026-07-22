from datetime import datetime
from dataclasses import dataclass, field
from uuid import UUID

from src.library.domain.value_objects.shelf_name import ShelfName
from src.library.domain.value_objects.color import Color
from src.library.domain.entities.shelf_book_association import ShelfBookAssociation


@dataclass
class Shelf:
    id: UUID
    name: ShelfName
    color: Color
    book_associations: list[ShelfBookAssociation] = field(default_factory=list)
    is_starred: bool = False
    is_deleted: bool = False
    deleted_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def book_ids(self) -> list[UUID]:
        return [assoc.book_id for assoc in self.book_associations]

    def rename(self, new_name: ShelfName) -> None:
        self.name = new_name
        self.updated_at = datetime.now()

    def change_color(self, new_color: Color) -> None:
        self.color = new_color
        self.updated_at = datetime.now()

    def toggle_star(self) -> None:
        self.is_starred = not self.is_starred
        self.updated_at = datetime.now()

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()

    def restore(self) -> None:
        self.is_deleted = False
        self.deleted_at = None
        self.updated_at = datetime.now()

    def add_book(self, book_id: UUID) -> None:
        if not any(a.book_id == book_id for a in self.book_associations):
            position = len(self.book_associations)
            association = ShelfBookAssociation(
                shelf_id=self.id,
                book_id=book_id,
                position=position,
            )
            self.book_associations.append(association)
            self.updated_at = datetime.now()

    def remove_book(self, book_id: UUID) -> None:
        self.book_associations = [
            a for a in self.book_associations if a.book_id != book_id
        ]
        self.updated_at = datetime.now()

    def has_book(self, book_id: UUID) -> bool:
        return any(a.book_id == book_id for a in self.book_associations)

    def reorder_books(self, book_ids: list[UUID]) -> None:
        current_ids = {a.book_id for a in self.book_associations}
        if set(book_ids) != current_ids:
            raise ValueError(
                "Provided book IDs do not match the current set of book IDs in the shelf"
            )

        id_to_assoc = {a.book_id: a for a in self.book_associations}
        self.book_associations = []
        for position, book_id in enumerate(book_ids):
            assoc = id_to_assoc[book_id]
            self.book_associations.append(
                ShelfBookAssociation(
                    shelf_id=self.id,
                    book_id=book_id,
                    position=position,
                )
            )
        self.updated_at = datetime.now()

    def book_count(self) -> int:
        return len(self.book_associations)