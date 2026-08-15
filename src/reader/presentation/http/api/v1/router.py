from fastapi import APIRouter

from src.reader.presentation.http.api.v1.endpoints.sessions.router import router as sessions_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(sessions_router)