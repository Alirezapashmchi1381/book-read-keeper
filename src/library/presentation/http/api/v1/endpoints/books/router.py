from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File

from src.library.application.dtos.create_book_dto import CreateBookInputDto
from src.library.application.dtos.update_book_metadata_dto import UpdateBookMetadataInputDto
from src.library.application.dtos.search_books_dto import SearchBooksInputDto, BookOutputDto
from src.library.application.dtos.upload_book_file_dto import UploadBookFileInputDto
from src.library.application.dtos.upload_book_cover_dto import UploadBookCoverInputDto
from src.library.domain.exceptions import ResourceCorruptedError
from src.library.application.use_cases.create_book import CreateBookUseCase
from src.library.application.use_cases.update_book_metadata import UpdateBookMetadataUseCase
from src.library.application.use_cases.upload_book_file import UploadBookFileUseCase
from src.library.application.use_cases.upload_book_cover import UploadBookCoverUseCase
from src.library.application.use_cases.star_book import StarBookUseCase
from src.library.application.use_cases.delete_book import DeleteBookUseCase
from src.library.application.use_cases.restore_book import RestoreBookUseCase
from src.library.application.use_cases.search_books import SearchBooksUseCase
from src.library.application.use_cases.get_book import GetBookUseCase
from src.library.presentation.http.api.v1.endpoints.books.models import (
    CreateBookRequest,
    UpdateBookMetadataRequest,
    BookResponse,
    FullBookResponse,
    ShelfBriefResponse,
    BookFileResponse,
    BookCoverResponse,
    SearchBooksResponse,
)
from src.library.presentation.http.response import make_response
from src.library.core.dependencies import (
    get_create_book_use_case,
    get_update_book_metadata_use_case,
    get_upload_book_file_use_case,
    get_upload_book_cover_use_case,
    get_star_book_use_case,
    get_delete_book_use_case,
    get_restore_book_use_case,
    get_search_books_use_case,
    get_get_book_use_case,
    get_current_user_id,
    get_library_uow,
)
from src.library.infrastructure.sql.unit_of_work.library import SQLAlchemyLibraryUnitOfWork

router = APIRouter(prefix="/books", tags=["books"])


def _book_to_response(book) -> BookResponse:
    return BookResponse(
        id=book.id,
        title=book.metadata.title,
        author_first_name=book.metadata.author.first_name,
        author_last_name=book.metadata.author.last_name,
        isbn=str(book.metadata.isbn),
        language=book.metadata.language.code,
        color=book.metadata.color.hex_value,
        description=book.metadata.description,
        is_starred=book.is_starred,
        is_deleted=book.is_deleted,
        created_at=book.created_at,
        updated_at=book.updated_at,
    )


@router.post("")
async def create_book(
    body: CreateBookRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: CreateBookUseCase = Depends(get_create_book_use_case),
):
    book = await use_case.execute(
        CreateBookInputDto(
            author_first_name=body.author_first_name,
            author_last_name=body.author_last_name,
            isbn=body.isbn,
            title=body.title,
            language=body.language,
            color=body.color,
            description=body.description,
        )
    )
    return make_response(data=_book_to_response(book))


@router.get("/{book_id}")
async def get_book(
    book_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: GetBookUseCase = Depends(get_get_book_use_case),
    uow: SQLAlchemyLibraryUnitOfWork = Depends(get_library_uow),
):
    book = await use_case.execute(book_id)
    async with uow:
        shelves = await uow.shelves.query.find_shelves_by_book_id(book_id)

    return make_response(
        data=FullBookResponse(
            **_book_to_response(book).model_dump(),
            shelves=[
                ShelfBriefResponse(id=s.id, name=s.name.name, color=s.color.hex_value)
                for s in shelves
            ],
        )
    )


@router.patch("/{book_id}")
async def update_book_metadata(
    book_id: UUID,
    body: UpdateBookMetadataRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: UpdateBookMetadataUseCase = Depends(get_update_book_metadata_use_case),
):
    book = await use_case.execute(
        UpdateBookMetadataInputDto(
            book_id=book_id,
            author_first_name=body.author_first_name,
            author_last_name=body.author_last_name,
            isbn=body.isbn,
            title=body.title,
            language=body.language,
            color=body.color,
            description=body.description,
            is_starred=body.is_starred,
        )
    )
    return make_response(data=_book_to_response(book))


@router.post("/{book_id}/file")
async def upload_book_file(
    book_id: UUID,
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
    use_case: UploadBookFileUseCase = Depends(get_upload_book_file_use_case),
):
    content = await file.read()
    filename = file.filename or "file"
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
    book = await use_case.execute(
        UploadBookFileInputDto(
            book_id=book_id,
            content=content,
            format=ext,
            mime_type=file.content_type or "application/octet-stream",
        )
    )
    if book.book_file is None:
        raise ResourceCorruptedError("Book file was not uploaded")
    book_file = book.book_file
    return make_response(
        data=BookFileResponse(
            storage_key=book_file.storage_key.value,
            format=book_file.format.value,
            checksum_algorithm=book_file.checksum.algorithm,
            checksum_value=book_file.checksum.value,
            size_bytes=book_file.size.value,
            mime_type=book_file.mime_type.value,
        )
    )


@router.post("/{book_id}/cover")
async def upload_book_cover(
    book_id: UUID,
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
    use_case: UploadBookCoverUseCase = Depends(get_upload_book_cover_use_case),
):
    content = await file.read()
    book = await use_case.execute(
        UploadBookCoverInputDto(
            book_id=book_id,
            content=content,
            mime_type=file.content_type or "image/jpeg",
        )
    )
    if book.cover is None:
        raise ResourceCorruptedError("Cover was not uploaded")
    cover = book.cover
    return make_response(
        data=BookCoverResponse(
            storage_key=cover.storage_key.value,
            width=cover.width,
            height=cover.height,
            generated=cover.generated,
        )
    )


@router.post("/{book_id}/star")
async def star_book(
    book_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: StarBookUseCase = Depends(get_star_book_use_case),
):
    await use_case.execute(book_id)
    return make_response(message="Book starred successfully")


@router.delete("/{book_id}")
async def delete_book(
    book_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: DeleteBookUseCase = Depends(get_delete_book_use_case),
):
    await use_case.execute(book_id)
    return make_response(message="Book deleted successfully")


@router.post("/{book_id}/restore")
async def restore_book(
    book_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: RestoreBookUseCase = Depends(get_restore_book_use_case),
):
    await use_case.execute(book_id)
    return make_response(message="Book restored successfully")


@router.get("")
async def search_books(
    title: str,
    user_id: UUID = Depends(get_current_user_id),
    use_case: SearchBooksUseCase = Depends(get_search_books_use_case),
):
    books: list[BookOutputDto] = await use_case.execute(SearchBooksInputDto(title=title))
    items = [
        BookResponse(
            id=book.id,
            title=book.title,
            author_first_name=book.author_first_name,
            author_last_name=book.author_last_name,
            isbn=book.isbn,
            language=book.language,
            color=book.color,
            description=book.description,
            is_starred=book.is_starred,
            is_deleted=book.is_deleted,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )
        for book in books
    ]
    return make_response(data=SearchBooksResponse(items=items, total=len(items)))
