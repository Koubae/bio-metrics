from abc import ABC, abstractmethod

from src.account.domain.entities import Account, AccountWithPassword
from src.core.domain.ports import AsyncRepository
from src.core.domain.types import Model


class AccountRepository(AsyncRepository[Account, Model], ABC):

    @abstractmethod
    async def new_account(self, entity: Account, password_hash: str) -> Account: ...

    @abstractmethod
    async def find_by_username(self, username: str) -> Account | None: ...

    @abstractmethod
    async def find_by_username_or_fail(self, username: str) -> Account: ...

    @abstractmethod
    async def find_by_username_for_login(
        self, username: str
    ) -> AccountWithPassword | None: ...

    @abstractmethod
    async def list_accounts(self, limit: int, offset: int) -> list[Account]: ...
