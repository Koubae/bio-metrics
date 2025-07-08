from fastapi import APIRouter, Depends

from dependencies.providers import get_account_service
from src.account.application.account_service import AccountService
from src.auth.application.auth_handlers import (
    SignUpRequest,
    LoginRequest,
    LoginResponse,
    SignUpResponse,
    SignUpHandler,
)
from src.settings import Settings


class AuthController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            path="/signup", endpoint=self.signup, methods=["POST"]
        )
        self.router.add_api_route(path="/login", endpoint=self.login, methods=["POST"])

    async def signup(
        self,
        request: SignUpRequest,
        service: AccountService = Depends(get_account_service),
    ) -> SignUpResponse:
        # TODO add erro handling
        handler = SignUpHandler(request, service)

        response = await handler.handle()
        return response

    async def login(self, request: LoginRequest) -> LoginResponse:
        # TODO
        return LoginResponse(access_token="token", expires=1.0)
