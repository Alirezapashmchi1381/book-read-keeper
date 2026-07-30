from fastapi import Request
from fastapi.responses import JSONResponse

from src.library.domain.exceptions import (
    LibraryError,
    BookNotFoundError,
    ShelfNotFoundError,
    BookAlreadyDeletedError,
    BookNotDeletedError,
    ShelfAlreadyDeletedError,
    ShelfNotDeletedError,
    DuplicateBookInShelfError,
    BookNotInShelfError,
    ShelfLimitExceededError,
    FileStorageError,
    InvalidFileError,
    ResourceCorruptedError,
)
from src.library.presentation.http.response import make_error


async def book_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message=str(exc), code=404)
    return JSONResponse(status_code=404, content=body.model_dump())


async def shelf_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message=str(exc), code=404)
    return JSONResponse(status_code=404, content=body.model_dump())


async def book_not_in_shelf_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message=str(exc), code=404)
    return JSONResponse(status_code=404, content=body.model_dump())


async def conflict_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message=str(exc), code=409)
    return JSONResponse(status_code=409, content=body.model_dump())


async def bad_request_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message=str(exc), code=400)
    return JSONResponse(status_code=400, content=body.model_dump())


async def resource_corrupted_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message=str(exc), code=500)
    return JSONResponse(status_code=500, content=body.model_dump())


async def library_error_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message=str(exc), code=400)
    return JSONResponse(status_code=400, content=body.model_dump())


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message="An unexpected error occurred", code=500)
    return JSONResponse(status_code=500, content=body.model_dump())
