from fastapi import APIRouter

from src.api.infrastructure.controllers import IndexController, AuthController

__all__ = ("get_router",)


def get_router() -> APIRouter:
    router = APIRouter()

    index_controller = IndexController()
    router.include_router(index_controller.router, tags=["index"])

    api_v1 = APIRouter(prefix="/api/v1")

    auth_controller = AuthController()
    api_v1.include_router(auth_controller.router, prefix="/auth", tags=["auth"])

    router.include_router(api_v1)
    return router
