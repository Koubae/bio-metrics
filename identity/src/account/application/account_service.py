from src.account.domain.entities import Account, AccountWithPassword
from src.account.domain.ports import AccountRepository
from src.auth.domain.entities import Role
from src.auth.domain.ports import PasswordHasher, AccessTokenGenerator


class AccountService:
    def __init__(
        self, account_repository: AccountRepository, password_hasher: PasswordHasher
    ) -> None:
        self.account_repository: AccountRepository = account_repository
        self.password_hasher: PasswordHasher = password_hasher

    async def create_account(
        self, username: str, password: str, role: Role | None = None
    ) -> Account:
        if role is None:
            role_assigned = Role.USER
        else:
            role_assigned = role

        password_hash = self.password_hasher.hash_password(password)
        entity = Account(id=None, username=username, role=role_assigned)
        await self.account_repository.new_account(
            entity=entity, password_hash=password_hash
        )
        return entity

    async def get_account(self, username: str) -> Account | None:
        account = await self.account_repository.find_by_username_or_fail(username)
        return account

    async def get_account_or_none(self, username: str) -> Account | None:
        account = await self.account_repository.find_by_username(username)
        if account is None:
            return None
        return account

    async def get_account_for_login(self, username: str) -> AccountWithPassword | None:
        account = await self.account_repository.find_by_username_for_login(username)
        return account
