from fastapi import FastAPI

from src.annotations.presentation.http.api.v1.router import v1_router
from src.annotations.presentation.http.middleware.register_exception_handler import (
    register_exception_handlers,
)


def create_annotations_app() -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(v1_router, prefix="/api")
    return app