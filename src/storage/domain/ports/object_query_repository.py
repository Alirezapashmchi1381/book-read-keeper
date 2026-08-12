from typing import Protocol

from src.storage.domain.entities.object import Object
from src.storage.domain.value_objects.object_key import ObjectKey


class ObjectQueryRepository(Protocol):
    async def find_by_key(self, key: ObjectKey) -> Object | None: ...

    async def list_all(self) -> list[Object]: ...

    async def search_by_prefix(self, prefix: str) -> list[Object]: ...