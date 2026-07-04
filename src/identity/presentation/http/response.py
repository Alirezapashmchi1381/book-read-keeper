from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: T | None = None
    meta_data: dict = {}


def make_response(
    *,
    data: T | None = None,
    message: str = "Success",
    code: int = 200,
    meta_data: dict | None = None,
) -> ApiResponse[T]:
    return ApiResponse(code=code, message=message, data=data, meta_data=meta_data or {})


def make_error(*, message: str, code: int = 400) -> ApiResponse[None]:
    return ApiResponse(code=code, message=message, data=None, meta_data={})
