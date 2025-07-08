import logging

from fastapi import HTTPException
from pydantic import BaseModel, Field

from src.account.application.account_service import AccountService
from src.account.domain.entities import Account
from src.auth.domain.entities import Role
from src.core.domain.exceptions import RepositoryDuplicateRowException


logger = logging.getLogger(__name__)


class SignUpRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, repr=False)
    role: Role | None = Field(None, description="User role")


class SignUpResponse(BaseModel):
    id: int
    username: str
    role: Role


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, repr=False)


class LoginResponse(BaseModel):
    access_token: str
    expires: float


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
                f"Duplicate account {self.request.username} : {error}",
                extra={"extra": {"username": self.request.username}},
            )
            raise HTTPException(
                status_code=409,
                detail={"error": f"Account '{self.request.username}' already exists!"},
            )

        return SignUpResponse(
            id=account.id, username=account.username, role=account.role
        )
