from fastapi import APIRouter
from starlette.responses import HTMLResponse

from src.auth.application.auth_handlers import SignUpRequest, LoginRequest, LoginResponse, SignUpResponse
from src.auth.domain.entities import AccessToken
from src.settings import Settings


class AuthController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(path="/signup", endpoint=self.signup, methods=["POST"])
        self.router.add_api_route(path="/login", endpoint=self.login, methods=["POST"])

    async def signup(self, request: SignUpRequest) -> SignUpResponse:
        # TODO
        return SignUpResponse(user_id=1, role="admin")

    async def login(self, request: LoginRequest) -> LoginResponse:
        # TODO
        return LoginResponse(access_token="token", expires=1.0)

