import logging

from fastapi import HTTPException
from pydantic import BaseModel, Field

from src.account.application.account_service import AccountService
from src.account.domain.entities import Account
from src.auth.application.auth_service import AuthService
from src.auth.domain.entities import Role, AccessToken
from src.auth.domain.exceptions import AuthPasswordInvalid
from src.core.domain.exceptions import (
    RepositoryDuplicateRowException,
    RepositoryCreateException,
    RepositoryDatabaseConnectionError,
    UNEXPECTED_ERROR_MESSAGE,
    RepositoryEntityNotFound,
)

logger = logging.getLogger(__name__)


class SignUpRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, repr=False)
    role: Role | None = Field(None, description="User role")


class SignUpResponse(BaseModel):
    id: int
    username: str
    role: Role


class SignUpHandler:
    def __init__(self, request: SignUpRequest, account_service: AccountService):
        self.request: SignUpRequest = request
        self.account_service: AccountService = account_service

    async def handle(self) -> SignUpResponse:
        try:
            account: Account = await self.account_service.create_account(
                self.request.username, self.request.password, self.request.role
            )
        except RepositoryDuplicateRowException as error:
            logger.warning(
                f"Signup failed, duplicate account {self.request.username} : {repr(error)}",
                extra={"extra": {"username": self.request.username}},
            )
            raise HTTPException(
                status_code=409,
                detail={"error": f"Account '{self.request.username}' already exists!"},
            )

        except (RepositoryCreateException, RepositoryDatabaseConnectionError) as error:
            logger.exception(
                f"Signup failed, Unexpected exception, account {self.request.username} : {repr(error)}",
                extra={"extra": {"username": self.request.username}},
            )
            raise HTTPException(
                status_code=500, detail={"error": UNEXPECTED_ERROR_MESSAGE}
            )

        return SignUpResponse(
            id=account.id, username=account.username, role=account.role
        )


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, repr=False)


class LoginResponse(BaseModel):
    access_token: str
    role: Role
    expires: float


class LoginHandler:
    def __init__(self, request: LoginRequest, auth_service: AuthService):
        self.request: LoginRequest = request
        self.auth_service: AuthService = auth_service

    async def handle(self) -> LoginResponse:
        try:
            access_token: AccessToken = await self.auth_service.login(
                self.request.username, self.request.password
            )
        except RepositoryEntityNotFound as error:
            logger.info(
                f"Login failed, Account {self.request.username} not found: {repr(error)}",
                extra={"extra": {"username": self.request.username}},
            )
            raise HTTPException(
                status_code=401,
                detail={"error": f"Account '{self.request.username}' does not exists!"},
            )

        except AuthPasswordInvalid as error:
            logger.info(
                f"Login failed, invalid password for account {self.request.username}: {repr(error)}",
                extra={"extra": {"username": self.request.username}},
            )
            raise HTTPException(
                status_code=401,
                detail={"error": "Password is incorrect!"},
            )
        except RepositoryDatabaseConnectionError as error:
            logger.exception(
                f"Login failed, Unexpected exception {self.request.username} : {repr(error)}",
                extra={"extra": {"username": self.request.username}},
            )
            raise HTTPException(
                status_code=500, detail={"error": UNEXPECTED_ERROR_MESSAGE}
            )

        return LoginResponse(
            access_token=access_token.access_token, role=Role.USER, expires=1234567890
        )
