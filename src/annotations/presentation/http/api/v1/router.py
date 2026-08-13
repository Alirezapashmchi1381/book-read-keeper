from fastapi import APIRouter

from src.annotations.presentation.http.api.v1.endpoints.highlights.router import router as highlights_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(highlights_router)