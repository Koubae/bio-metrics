from src.account.domain.entities import Account
from src.account.domain.ports import AccountRepository
from src.auth.domain.entities import Role
from src.auth.domain.ports import PasswordHasher


class AccountService:
    def __init__(
        self, account_repository: AccountRepository, password_hasher: PasswordHasher
    ):
        self.account_repository: AccountRepository = account_repository
        self.password_hasher: PasswordHasher = password_hasher

    async def create_account(
        self, username: str, password: str, role: Role | None = None
    ) -> Account:
        password_hash = self.password_hasher.hash_password(password)
        entity = Account(id=None, username=username, role=role)
        await self.account_repository.new_account(
            entity=entity, password_hash=password_hash
        )
        return entity
