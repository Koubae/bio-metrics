from fastapi import APIRouter, Depends

from dependencies.providers import provide_account_service
from src.account.application.account_handlers import (
    GetAccountRequest,
    GetAccountHandler,
)
from src.account.application.account_service import AccountService
from src.account.domain.entities import Account
from src.auth.application.secure import restrict
from src.auth.domain.entities import AccessToken, Role
from src.settings import Settings


class AccountController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            path="/{username}", endpoint=self.get, methods=["GET"]
        )
        self.router.add_api_route(path="/", endpoint=self.list, methods=["GET"])
        self.router.add_api_route(
            path="/update-role", endpoint=self.update_role, methods=["PATCH"]
        )

    @staticmethod
    async def get(
        username: str,
        access_token: AccessToken = Depends(
            restrict((Role.ADMIN, Role.LAB_SCIENTIST, Role.DOCTOR, Role.USER))
        ),
        service: AccountService = Depends(provide_account_service),
    ) -> Account:
        request = GetAccountRequest(username=username, access_token=access_token)
        handler = GetAccountHandler(request, service)
        response = await handler.handle()
        return response

    @staticmethod
    async def list(
        service: AccountService = Depends(provide_account_service),
    ) -> None:
        raise NotImplementedError("TODO")

    @staticmethod
    async def update_role(
        service: AccountService = Depends(provide_account_service),
    ) -> None:
        raise NotImplementedError("TODO")
