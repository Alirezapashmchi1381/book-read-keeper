from datetime import datetime
from dataclasses import dataclass, field
from uuid import UUID

from src.library.domain.entities.book import Book
from src.library.domain.value_objects.shelf_name import ShelfName
from src.library.domain.value_objects.color import Color
from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.isbn import ISBN
from src.library.domain.value_objects.language import Language
from src.library.domain.value_objects.book_metadata import BookMetadata


@dataclass
class Shelf:
    id: UUID
    name: ShelfName
    color: Color
    books: list[Book] = field(default_factory=list)
    is_starred: bool = False
    is_deleted: bool = False
    deleted_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

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

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        self.updated_at = datetime.now()

    def remove_book(self, book_id: UUID) -> Book | None:
        for i, book in enumerate(self.books):
            if book.id == book_id:
                removed = self.books.pop(i)
                self.updated_at = datetime.now()
                return removed
        return None

    def get_book(self, book_id: UUID) -> Book | None:
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def reorder_books(self, book_ids: list[UUID]) -> None:
        if len(book_ids) != len(self.books):
            raise ValueError(
                "Number of book IDs must match number of books in the shelf"
            )

        book_map = {book.id: book for book in self.books}
        new_order: list[Book] = []
        for book_id in book_ids:
            if book_id not in book_map:
                raise ValueError(f"Book with ID {book_id} not found in shelf")
            new_order.append(book_map[book_id])

        self.books = new_order
        self.updated_at = datetime.now()

    def rename_book(self, book_id: UUID, new_title: str) -> None:
        book = self.get_book(book_id)
        if book is None:
            raise ValueError(f"Book with ID {book_id} not found in shelf")

        new_metadata = BookMetadata(
            author=book.metadata.author,
            isbn=book.metadata.isbn,
            title=new_title,
            language=book.metadata.language,
            shelf_name=book.metadata.shelf_name,
            color=book.metadata.color,
            description=book.metadata.description,
        )
        book.metadata = new_metadata
        book.updated_at = datetime.now()
        self.updated_at = datetime.now()

    def book_count(self) -> int:
        return len(self.books)

    def starred_books(self) -> list[Book]:
        return [book for book in self.books if book.is_starred]