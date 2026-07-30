from unittest.mock import AsyncMock
from uuid import UUID, uuid4
from datetime import datetime

from src.library.domain.entities.book import Book
from src.library.domain.entities.shelf import Shelf
from src.library.domain.value_objects.book_metadata import BookMetadata
from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.isbn import ISBN
from src.library.domain.value_objects.language import Language
from src.library.domain.value_objects.color import Color
from src.library.domain.value_objects.shelf_name import ShelfName
from src.library.domain.value_objects.book_file import BookFile
from src.library.domain.value_objects.cover import Cover
from src.library.domain.value_objects.storage_key import StorageKey
from src.library.domain.value_objects.file_format import FileFormat
from src.library.domain.value_objects.file_size import FileSize
from src.library.domain.value_objects.mime_type import MimeType
from src.library.domain.value_objects.checksum import Checksum


class FakeSubUoW:
    def __init__(self) -> None:
        self.query = AsyncMock()
        self.command = AsyncMock()


class FakeLibraryUnitOfWork:
    def __init__(self) -> None:
        self.books = FakeSubUoW()
        self.shelves = FakeSubUoW()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> "FakeLibraryUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.committed = True
        else:
            self.rolled_back = True

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True


class FakeFileStorageService:
    def __init__(self) -> None:
        self.stored_files: list[tuple[UUID, bytes, str]] = []
        self.stored_covers: list[tuple[UUID, bytes, str]] = []
        self.next_book_file: BookFile | None = None
        self.next_cover: Cover | None = None

    async def store_book_file(
        self, book_id: UUID, content: bytes, format: FileFormat
    ) -> BookFile:
        self.stored_files.append((book_id, content, format.value))
        if self.next_book_file:
            return self.next_book_file
        return BookFile(
            storage_key=StorageKey(f"books/{book_id}/file.{format.value}"),
            format=format,
            checksum=Checksum(algorithm="sha256", value="fake-checksum"),
            size=FileSize(len(content)),
            mime_type=MimeType("application/octet-stream"),
        )

    async def store_cover(
        self, book_id: UUID, content: bytes, mime_type: MimeType
    ) -> Cover:
        self.stored_covers.append((book_id, content, mime_type.value))
        if self.next_cover:
            return self.next_cover
        return Cover(
            storage_key=StorageKey(f"books/{book_id}/cover"),
            width=200,
            height=300,
            generated=False,
        )

    async def delete_file(self, storage_key: str) -> None:
        pass

    async def get_download_url(self, storage_key: str) -> str:
        return f"https://storage.example.com/{storage_key}"


def make_book(
    *,
    title: str = "Test Book",
    author_first: str = "John",
    author_last: str = "Doe",
    isbn: str = "9780747532699",
    language: str = "en",
    color: str = "#FF5733",
    description: str | None = "A test book.",
    is_starred: bool = False,
    is_deleted: bool = False,
    book_file: BookFile | None = None,
    cover: Cover | None = None,
) -> Book:
    book = Book.create(
        metadata=BookMetadata(
            author=Author(first_name=author_first, last_name=author_last),
            isbn=ISBN(isbn),
            title=title,
            language=Language(language),
            color=Color(color),
            description=description,
        ),
    )
    if is_starred:
        book.mark_as_starred()
    if is_deleted:
        book.soft_delete()
    if book_file:
        book.attach_book_file(book_file)
    if cover:
        book.attach_cover(cover)
    return book


def make_shelf(
    *,
    name: str = "Favorites",
    color: str = "#FF5733",
    book_ids: list[UUID] | None = None,
    is_starred: bool = False,
    is_deleted: bool = False,
) -> Shelf:
    shelf = Shelf(
        id=uuid4(),
        name=ShelfName(name),
        color=Color(color),
    )
    if is_starred:
        shelf.toggle_star()
    if is_deleted:
        shelf.soft_delete()
    if book_ids:
        for bid in book_ids:
            shelf.add_book(bid)
    return shelf