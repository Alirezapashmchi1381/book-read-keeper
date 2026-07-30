import pytest
from uuid import uuid4

from src.library.application.dtos.upload_book_file_dto import UploadBookFileInputDto
from src.library.application.use_cases.upload_book_file import UploadBookFileUseCase
from src.library.domain.exceptions import BookNotFoundError
from tests.library.application.use_cases.factories import make_book


@pytest.fixture
def use_case(fake_uow, fake_file_storage) -> UploadBookFileUseCase:
    return UploadBookFileUseCase(uow=fake_uow, file_storage=fake_file_storage)


async def test_upload_book_file_attaches_file(use_case, fake_uow, fake_file_storage):
    book = make_book()
    fake_uow.books.query.find_by_id.return_value = book

    dto = UploadBookFileInputDto(
        book_id=book.id,
        content=b"book file content",
        format="pdf",
        mime_type="application/pdf",
    )
    result = await use_case.execute(dto)

    assert result.book_file is not None
    assert fake_file_storage.stored_files[0][0] == book.id


async def test_upload_book_file_raises_if_not_found(use_case, fake_uow, fake_file_storage):
    fake_uow.books.query.find_by_id.return_value = None

    dto = UploadBookFileInputDto(
        book_id=uuid4(),
        content=b"content",
        format="pdf",
        mime_type="application/pdf",
    )
    with pytest.raises(BookNotFoundError):
        await use_case.execute(dto)