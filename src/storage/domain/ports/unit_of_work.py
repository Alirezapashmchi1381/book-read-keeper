from typing import Protocol

from src.storage.domain.ports.bucket_command_repository import BucketCommandRepository
from src.storage.domain.ports.bucket_query_repository import BucketQueryRepository
from src.storage.domain.ports.object_command_repository import ObjectCommandRepository
from src.storage.domain.ports.object_query_repository import ObjectQueryRepository


class BucketUoW(Protocol):
    query: BucketQueryRepository
    command: BucketCommandRepository


class ObjectUoW(Protocol):
    query: ObjectQueryRepository
    command: ObjectCommandRepository


class StorageUnitOfWork(Protocol):
    buckets: BucketUoW
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