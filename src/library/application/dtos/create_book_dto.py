from dataclasses import dataclass

from src.library.domain.value_objects.book_metadata import BookMetadata
from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.isbn import ISBN
from src.library.domain.value_objects.language import Language
from src.library.domain.value_objects.color import Color


@dataclass(frozen=True)
class CreateBookInputDto:
    author_first_name: str
    author_last_name: str
    isbn: str
    title: str
    language: str
    color: str
    description: str | None = None

    def to_metadata(self) -> BookMetadata:
        return BookMetadata(
            author=Author(
                first_name=self.author_first_name,
                last_name=self.author_last_name,
            ),
            isbn=ISBN(self.isbn),
            title=self.title,
            language=Language(self.language),
            color=Color(self.color),
            description=self.description,
        )