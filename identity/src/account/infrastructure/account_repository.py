from sqlalchemy import select

from src.account.domain.entities import Account, AccountWithPassword
from src.account.domain.ports import AccountRepository
from src.account.infrastructure.models import AccountModel, AccountMapper
from src.core.domain.exceptions import RepositoryEntityNotFound
from src.core.infrastructure.database.async_repository import AsyncSqlalchemyRepository


class AccountRepositoryAdapter(
    AsyncSqlalchemyRepository[Account, AccountModel], AccountRepository
):
    _entity: type[Account] = Account
    _model: type[AccountModel] = AccountModel
    _mapper: type[AccountMapper] = AccountMapper

    async def new_account(self, entity: Account, password_hash: str) -> None:
        model = self._model(**self._mapper.to_dict(entity))
        model.password = password_hash
        await self._create(entity, model)

    async def find_by_username(self, username: str) -> Account | None:
        stmt = select(AccountModel).where(AccountModel.username == username)
        result = await self._session.execute(stmt)

        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._mapper.to_entity(model)

    async def find_by_username_or_fail(self, username: str) -> Account:
        """
        Raises
            - RepositoryEntityNotFound: if the entity was not found
        """
        entity = await self.find_by_username(username)
        if not entity:
            raise RepositoryEntityNotFound(model=self._model, values=(username,))
        return entity

    async def find_by_username_for_login(
        self, username: str
    ) -> AccountWithPassword | None:
        """
        Raises
            - RepositoryEntityNotFound: if the entity was not found
        """
        stmt = select(AccountModel).where(AccountModel.username == username)
        result = await self._session.execute(stmt)

        model = result.scalar_one_or_none()
        if model is None:
            raise RepositoryEntityNotFound(model=self._model, values=(username,))
        return self._mapper.to_entity_with_secret(model)

    async def list_accounts(self, limit: int, offset: int) -> list[Account]:
        stmt = (
            select(AccountModel).order_by(AccountModel.id).limit(limit).offset(offset)
        )
        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        accounts = [self._mapper.to_entity(row) for row in rows]
        return accounts
