from abc import ABC, abstractmethod
from typing import Generic

from src.core.domain.types import DBPrimaryKey, Entity, Model


class AsyncRepository(ABC, Generic[Entity, Model]):
    @abstractmethod
    async def find_by_pk(self, pk: DBPrimaryKey) -> Entity | None:
        pass

    @abstractmethod
    async def create(self, domain: Entity) -> None:
        pass

    @abstractmethod
    async def update(self, domain: Entity) -> bool:
        pass

    @abstractmethod
    async def delete_by_pk(self, pk: DBPrimaryKey) -> bool:
        pass
