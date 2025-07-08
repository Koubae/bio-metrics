from src.account.domain.entities import Account
from src.account.domain.ports import AccountRepository
from src.account.infrastructure.models import AccountModel, AccountMapper
from src.auth.domain.entities import Role
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
