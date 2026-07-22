from dataclasses import dataclass
from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.isbn import ISBN
from src.library.domain.value_objects.language import Language
from src.library.domain.value_objects.shelf_name import ShelfName


@dataclass(frozen=True)
class BookMetadata:
    author: Author
    isbn: ISBN
    title: str
    language: Language
    shelf_name: ShelfName
    description: str | None = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Title must not be empty")