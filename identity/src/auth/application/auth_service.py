from src.account.application.account_service import AccountService
from src.account.domain.entities import AccountWithPassword
from src.auth.domain.entities import AccessToken
from src.auth.domain.exceptions import AuthPasswordInvalid
from src.auth.domain.ports import PasswordHasher, AccessTokenGenerator


class AuthService:
    def __init__(
        self,
        password_hasher: PasswordHasher,
        auth: AccessTokenGenerator,
        account_service: AccountService,
    ):
        self.account_service: AccountService = account_service
        self.password_hasher: PasswordHasher = password_hasher
        self.auth: AccessTokenGenerator = auth

    async def login(self, username: str, password: str) -> AccessToken:
        account: AccountWithPassword = await self.account_service.get_account_for_login(
            username
        )

        password_hash = account.password
        password_match = self.password_hasher.verify_password(password, password_hash)
        if not password_match:
            raise AuthPasswordInvalid()

        access_token = self.auth.generate_access_token(
            account.id, username, account.role
        )
        return access_token
