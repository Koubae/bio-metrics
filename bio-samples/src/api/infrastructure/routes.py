from fastapi import APIRouter

from src.api.infrastructure.controllers import IndexController

__all__ = ("get_router",)



def get_router() -> APIRouter:
    router = APIRouter()

    index_controller = IndexController()
    router.include_router(index_controller.router, tags=["Index"])

    api_v1 = APIRouter(prefix="/api/v1")

    router.include_router(api_v1)
    return router
