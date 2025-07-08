from src.account.domain.entities import Account
from src.account.infrastructure.models import AccountModel, AccountMapper
from src.core.infrastructure.database.async_repository import AsyncSqlalchemyRepository


class AccountRepository(AsyncSqlalchemyRepository[Account, AccountModel]):
    _domain: type[Account] = Account
    _model: type[AccountModel] = AccountModel
    _mapper: type[AccountMapper] = AccountMapper
