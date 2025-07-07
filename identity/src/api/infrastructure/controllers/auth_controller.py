from fastapi import APIRouter
from starlette.responses import HTMLResponse

from src.settings import Settings


class AuthController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(path="/signup", endpoint=self.signup, methods=["POST"])
        self.router.add_api_route(path="/login", endpoint=self.login, methods=["POST"])

    async def signup(self) -> HTMLResponse:
        print("login")
        return "Ok"

    async def login(self) -> HTMLResponse:
        print("login")
        return "Ok"

