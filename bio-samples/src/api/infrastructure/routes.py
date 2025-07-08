from fastapi import APIRouter

from src.api.infrastructure.controllers import IndexController, SampleController

__all__ = ("get_router",)


def get_router() -> APIRouter:
    router = APIRouter()

    index_controller = IndexController()
    router.include_router(index_controller.router, tags=["Index"])

    api_v1 = APIRouter(prefix="/api/v1")

    sample_controller = SampleController()
    api_v1.include_router(
        sample_controller.router, prefix="/samples", tags=["Samples"]
    )

    router.include_router(api_v1)
    return router
