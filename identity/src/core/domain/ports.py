from abc import ABC, abstractmethod
from typing import Generic

from src.core.domain.types import Domain, Model, DBPrimaryKey


class AsyncRepository(ABC, Generic[Domain, Model]):
    @abstractmethod
    async def find_by_pk(self, pk: DBPrimaryKey) -> Domain | None:
        pass

    @abstractmethod
    async def create(self, domain: Domain) -> None:
        pass

    @abstractmethod
    async def update(self, domain: Domain) -> bool:
        pass

    @abstractmethod
    async def save(self, domain: Domain) -> Domain:
        pass

    @abstractmethod
    async def delete_by_pk(self, pk: DBPrimaryKey) -> bool:
        pass
