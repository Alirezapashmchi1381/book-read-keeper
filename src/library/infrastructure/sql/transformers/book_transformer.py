from typing import cast

from src.library.domain.entities.book import Book
from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.isbn import ISBN
from src.library.domain.value_objects.language import Language
from src.library.domain.value_objects.color import Color
from src.library.domain.value_objects.book_metadata import BookMetadata
from src.library.domain.value_objects.book_file import BookFile
from src.library.domain.value_objects.cover import Cover
from src.library.domain.value_objects.storage_key import StorageKey
from src.library.domain.value_objects.checksum import Checksum
from src.library.domain.value_objects.file_format import FileFormat
from src.library.domain.value_objects.file_size import FileSize
from src.library.domain.value_objects.mime_type import MimeType
from src.library.infrastructure.sql.models.book_model import BookModel


class BookTransformer:
    @staticmethod
    def to_domain(model: BookModel) -> Book:
        metadata = BookMetadata(
            author=Author(
                first_name=model.author_first_name,
                last_name=model.author_last_name,
            ),
            isbn=ISBN(model.isbn),
            title=model.title,
            language=Language(model.language),
            color=Color(model.color),
            description=model.description,
        )

        book_file: BookFile | None = None
        if model.storage_key is not None:
            if any(x is None for x in [
                model.file_format, model.checksum_algorithm,
                model.checksum_value, model.file_size, model.mime_type
            ]):
                raise ValueError(
                    f"Book {model.id} has storage_key but incomplete file metadata"
                )
            book_file = BookFile(
                storage_key=StorageKey(model.storage_key),
                format=FileFormat(cast(str, model.file_format)),
                checksum=Checksum(
                    algorithm=cast(str, model.checksum_algorithm),
                    value=cast(str, model.checksum_value),
                ),
                size=FileSize(cast(int, model.file_size)),
                mime_type=MimeType(cast(str, model.mime_type)),
            )

        cover: Cover | None = None
        if model.cover_storage_key is not None:
            if model.cover_width is None or model.cover_height is None:
                raise ValueError(
                    f"Book {model.id} has cover_storage_key "
                    "but incomplete cover dimensions"
                )
            cover = Cover(
                storage_key=StorageKey(model.cover_storage_key),
                width=model.cover_width,
                height=model.cover_height,
                generated=model.cover_generated,
            )

        return Book(
            id=model.id,
            metadata=metadata,
            book_file=book_file,
            cover=cover,
            is_starred=model.is_starred,
            is_deleted=model.is_deleted,
            deleted_at=model.deleted_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Book) -> BookModel:
        return BookModel(
            id=entity.id,
            title=entity.metadata.title,
            author_first_name=entity.metadata.author.first_name,
            author_last_name=entity.metadata.author.last_name,
            isbn=entity.metadata.isbn.value,
            language=entity.metadata.language.code,
            description=entity.metadata.description,
            color=entity.metadata.color.hex_value,
            storage_key=entity.book_file.storage_key.value if entity.book_file else None,
            file_format=entity.book_file.format.value if entity.book_file else None,
            checksum_algorithm=entity.book_file.checksum.algorithm if entity.book_file else None,
            checksum_value=entity.book_file.checksum.value if entity.book_file else None,
            file_size=entity.book_file.size.value if entity.book_file else None,
            mime_type=entity.book_file.mime_type.value if entity.book_file else None,
            cover_storage_key=entity.cover.storage_key.value if entity.cover else None,
            cover_width=entity.cover.width if entity.cover else None,
            cover_height=entity.cover.height if entity.cover else None,
            cover_generated=entity.cover.generated if entity.cover else False,
            is_starred=entity.is_starred,
            is_deleted=entity.is_deleted,
            deleted_at=entity.deleted_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )