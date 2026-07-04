from fastapi import Request
from fastapi.responses import JSONResponse

from src.identity.presentation.http.response import make_error


async def value_error_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message=str(exc), code=400)
    return JSONResponse(status_code=400, content=body.model_dump())


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    body = make_error(message="An unexpected error occurred", code=500)
    return JSONResponse(status_code=500, content=body.model_dump())
