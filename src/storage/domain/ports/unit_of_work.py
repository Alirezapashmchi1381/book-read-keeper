from typing import Protocol

from src.storage.domain.ports.object_command_repository import ObjectCommandRepository
from src.storage.domain.ports.object_query_repository import ObjectQueryRepository


class ObjectUoW(Protocol):
    query: ObjectQueryRepository
    command: ObjectCommandRepository


class StorageUnitOfWork(Protocol):
    objects: ObjectUoW

    async def __aenter__(self) -> "StorageUnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...