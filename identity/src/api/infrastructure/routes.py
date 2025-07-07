from fastapi import APIRouter

from src.api.infrastructure.controllers import IndexController

__all__ = ("get_router",)


def get_router() -> APIRouter:
    router = APIRouter()

    index_controller = IndexController()
    router.include_router(index_controller.router, tags=["index"])

    return router
