import logging

from fastapi import HTTPException
from pydantic import BaseModel, Field

from src.account.application.account_service import AccountService
from src.account.domain.entities import Account
from src.auth.domain.entities import AccessToken, Role
from src.core.domain.exceptions import RepositoryEntityNotFound

logger = logging.getLogger(__name__)


class GetAccountRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    access_token: AccessToken = Field(...)


class GetAccountHandler:
    def __init__(self, request: GetAccountRequest, account_service: AccountService):
        self.request: GetAccountRequest = request
        self.account_service: AccountService = account_service

    async def handle(self) -> Account:
        username = self.request.username
        try:
            account = await self.account_service.get_account(username)
        except RepositoryEntityNotFound as error:
            logger.info(
                f"Login failed, Account {username} not found: {repr(error)}",
                extra={"extra": {"username": username}},
            )
            raise HTTPException(
                status_code=404,
                detail={"error": f"Account '{username}' does not exists!"},
            )

        if self.request.access_token.username != username:
            if self.request.access_token.role not in (
                Role.ADMIN,
                Role.LAB_SCIENTIST,
                Role.DOCTOR,
            ):
                raise HTTPException(
                    status_code=403,
                    detail={"error": "You are not allowed to request this resource!"},
                )
        return account


class ListAccountHandler:
    def __init__(self, limit: int, offset: int, account_service: AccountService):
        self.limit: int = limit
        self.offset: int = offset
        self.account_service: AccountService = account_service

    async def handle(self) -> list[Account]:
        accounts = await self.account_service.list_accounts(self.limit, self.offset)
        return accounts


class UpdateRoleRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    role: Role = Field(...)


class UpdateRoleHandler:
    def __init__(
        self,
        request: UpdateRoleRequest,
        account_service: AccountService,
        access_token: AccessToken,
    ) -> None:
        self.request: UpdateRoleRequest = request
        self.account_service: AccountService = account_service
        self.access_token: AccessToken = access_token

    async def handle(self) -> Account:
        username = self.request.username
        try:
            account = await self.account_service.get_account(username)
        except RepositoryEntityNotFound as error:
            logger.info(
                f"Update Role failed, Account {username} not found: {repr(error)}",
                extra={"extra": {"username": username}},
            )
            raise HTTPException(
                status_code=404,
                detail={"error": f"Account '{username}' does not exists!"},
            )

        if account.role == self.request.role:
            logger.info(
                f"Update Role failed, Role on the same role {self.request.role} for user {account} ",
                extra={"extra": {"account": account}},
            )
            raise HTTPException(
                status_code=400,
                detail={"error": f"This user has already role '{self.request.role}'"},
            )

        account = await self.account_service.update_role(account, self.request.role)
        return account
