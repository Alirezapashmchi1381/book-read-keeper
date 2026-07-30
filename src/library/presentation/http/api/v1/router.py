from fastapi import APIRouter

from src.library.presentation.http.api.v1.endpoints.books.router import router as books_router
from src.library.presentation.http.api.v1.endpoints.shelves.router import router as shelves_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(books_router)
v1_router.include_router(shelves_router)
