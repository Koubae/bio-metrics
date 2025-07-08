from abc import ABC, abstractmethod

from src.account.domain.entities import Account
from src.auth.domain.entities import Role
from src.core.domain.ports import AsyncRepository
from src.core.domain.types import Model


class AccountRepository(AsyncRepository[Account, Model], ABC):

    @abstractmethod
    async def new_account(self, entity: Account, password_hash: str) -> Account: ...
