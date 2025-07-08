from fastapi import APIRouter

from src.api.infrastructure.controllers import IndexController, AuthController

__all__ = ("get_router",)

from src.api.infrastructure.controllers.account_controller import AccountController


def get_router() -> APIRouter:
    router = APIRouter()

    index_controller = IndexController()
    router.include_router(index_controller.router, tags=["Index"])

    api_v1 = APIRouter(prefix="/api/v1")

    auth_controller = AuthController()
    api_v1.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])

    account_controller = AccountController()
    api_v1.include_router(
        account_controller.router, prefix="/accounts", tags=["Account"]
    )

    router.include_router(api_v1)
    return router
