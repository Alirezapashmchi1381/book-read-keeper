from uuid import UUID

from fastapi import APIRouter, Depends

from src.library.application.dtos.create_shelf_dto import CreateShelfInputDto
from src.library.application.dtos.update_shelf_dto import UpdateShelfInputDto
from src.library.application.dtos.add_book_to_shelf_dto import AddBookToShelfInputDto
from src.library.application.dtos.remove_book_from_shelf_dto import RemoveBookFromShelfInputDto
from src.library.application.dtos.reorder_shelf_dto import ReorderShelfInputDto
from src.library.application.use_cases.create_shelf import CreateShelfUseCase
from src.library.application.use_cases.update_shelf import UpdateShelfUseCase
from src.library.application.use_cases.star_shelf import StarShelfUseCase
from src.library.application.use_cases.delete_shelf import DeleteShelfUseCase
from src.library.application.use_cases.restore_shelf import RestoreShelfUseCase
from src.library.application.use_cases.list_shelves import ListShelvesUseCase
from src.library.application.use_cases.add_book_to_shelf import AddBookToShelfUseCase
from src.library.application.use_cases.remove_book_from_shelf import RemoveBookFromShelfUseCase
from src.library.application.use_cases.reorder_shelf import ReorderShelfUseCase
from src.library.application.use_cases.get_shelf_books import GetShelfBooksUseCase
from src.library.presentation.http.api.v1.endpoints.shelves.models import (
    CreateShelfRequest,
    UpdateShelfRequest,
    AddBookToShelfRequest,
    ReorderShelfRequest,
    ShelfResponse,
    ShelfBookResponse,
)
from src.library.presentation.http.response import make_response
from src.library.core.dependencies import (
    get_create_shelf_use_case,
    get_update_shelf_use_case,
    get_star_shelf_use_case,
    get_delete_shelf_use_case,
    get_restore_shelf_use_case,
    get_list_shelves_use_case,
    get_add_book_to_shelf_use_case,
    get_remove_book_from_shelf_use_case,
    get_reorder_shelf_use_case,
    get_get_shelf_books_use_case,
    get_current_user_id,
)

router = APIRouter(prefix="/shelves", tags=["shelves"])


@router.post("")
async def create_shelf(
    body: CreateShelfRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: CreateShelfUseCase = Depends(get_create_shelf_use_case),
):
    shelf = await use_case.execute(
        CreateShelfInputDto(name=body.name, color=body.color)
    )
    return make_response(
        data=ShelfResponse(
            id=shelf.id,
            name=shelf.name.name,
            color=shelf.color.hex_value,
            book_count=shelf.book_count(),
            is_starred=shelf.is_starred,
            is_deleted=shelf.is_deleted,
            created_at=shelf.created_at,
            updated_at=shelf.updated_at,
        )
    )


@router.get("")
async def list_shelves(
    user_id: UUID = Depends(get_current_user_id),
    use_case: ListShelvesUseCase = Depends(get_list_shelves_use_case),
):
    shelves = await use_case.execute()
    items = [
        ShelfResponse(
            id=shelf.id,
            name=shelf.name,
            color=shelf.color,
            book_count=shelf.book_count,
            is_starred=shelf.is_starred,
            is_deleted=shelf.is_deleted,
            created_at=shelf.created_at,
            updated_at=shelf.updated_at,
        )
        for shelf in shelves
    ]
    return make_response(data=items)


@router.patch("/{shelf_id}")
async def update_shelf(
    shelf_id: UUID,
    body: UpdateShelfRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: UpdateShelfUseCase = Depends(get_update_shelf_use_case),
):
    shelf = await use_case.execute(
        UpdateShelfInputDto(
            shelf_id=shelf_id,
            name=body.name,
            color=body.color,
        )
    )
    return make_response(
        data=ShelfResponse(
            id=shelf.id,
            name=shelf.name.name,
            color=shelf.color.hex_value,
            book_count=shelf.book_count(),
            is_starred=shelf.is_starred,
            is_deleted=shelf.is_deleted,
            created_at=shelf.created_at,
            updated_at=shelf.updated_at,
        )
    )


@router.post("/{shelf_id}/star")
async def star_shelf(
    shelf_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: StarShelfUseCase = Depends(get_star_shelf_use_case),
):
    await use_case.execute(shelf_id)
    return make_response(message="Shelf starred successfully")


@router.delete("/{shelf_id}")
async def delete_shelf(
    shelf_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: DeleteShelfUseCase = Depends(get_delete_shelf_use_case),
):
    await use_case.execute(shelf_id)
    return make_response(message="Shelf deleted successfully")


@router.post("/{shelf_id}/restore")
async def restore_shelf(
    shelf_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: RestoreShelfUseCase = Depends(get_restore_shelf_use_case),
):
    await use_case.execute(shelf_id)
    return make_response(message="Shelf restored successfully")


@router.post("/{shelf_id}/books")
async def add_book_to_shelf(
    shelf_id: UUID,
    body: AddBookToShelfRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: AddBookToShelfUseCase = Depends(get_add_book_to_shelf_use_case),
):
    await use_case.execute(
        AddBookToShelfInputDto(shelf_id=shelf_id, book_id=body.book_id)
    )
    return make_response(message="Book added to shelf successfully")


@router.delete("/{shelf_id}/books/{book_id}")
async def remove_book_from_shelf(
    shelf_id: UUID,
    book_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: RemoveBookFromShelfUseCase = Depends(get_remove_book_from_shelf_use_case),
):
    await use_case.execute(
        RemoveBookFromShelfInputDto(shelf_id=shelf_id, book_id=book_id)
    )
    return make_response(message="Book removed from shelf successfully")


@router.put("/{shelf_id}/reorder")
async def reorder_shelf(
    shelf_id: UUID,
    body: ReorderShelfRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: ReorderShelfUseCase = Depends(get_reorder_shelf_use_case),
):
    await use_case.execute(
        ReorderShelfInputDto(shelf_id=shelf_id, book_ids=body.book_ids)
    )
    return make_response(message="Shelf reordered successfully")


@router.get("/{shelf_id}/books")
async def get_shelf_books(
    shelf_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: GetShelfBooksUseCase = Depends(get_get_shelf_books_use_case),
):
    books = await use_case.execute(shelf_id)
    items = [
        ShelfBookResponse(
            id=book.id,
            title=book.title,
            author_first_name=book.author_first_name,
            author_last_name=book.author_last_name,
            isbn=book.isbn,
            position=book.position,
            is_starred=book.is_starred,
        )
        for book in books
    ]
    return make_response(data=items)