from fastapi import APIRouter, Depends
from fastapi import Query

from dependencies.providers import provide_sample_service
from src.auth.application.secure import restrict
from src.auth.domain.entities import AccessToken, Role
from src.core.infrastructure.web.pagination import (
    PaginationParams,
    get_pagination_params,
)
from src.sample.application.sample_handlers import (
    CreateSampleRequest,
    CreateSampleHandler,
    GetSampleRequest,
    DeleteSampleRequest,
    GetSampleHandler,
    DeleteSampleHandler,
    ListPatientSamplesHandler,
)
from src.sample.application.sample_service import SampleService
from src.sample.domain.entities import Sample
from src.settings import Settings


class SampleController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(path="/", endpoint=self.post, methods=["POST"])
        self.router.add_api_route(
            path="/{sample_id}", endpoint=self.get, methods=["GET"]
        )
        self.router.add_api_route(
            path="/", endpoint=self.list_patient_samples, methods=["GET"]
        )
        self.router.add_api_route(
            path="/{sample_id}", endpoint=self.delete, methods=["DELETE"]
        )

    @staticmethod
    async def post(
        request: CreateSampleRequest,
        _: AccessToken = Depends(restrict((Role.ADMIN, Role.DOCTOR))),
        service: SampleService = Depends(provide_sample_service),
    ) -> Sample:
        handler = CreateSampleHandler(request, service)
        response = await handler.handle()
        return response

    @staticmethod
    async def get(
        sample_id: int,
        access_token: AccessToken = Depends(
            restrict((Role.ADMIN, Role.LAB_SCIENTIST, Role.DOCTOR, Role.USER))
        ),
        service: SampleService = Depends(provide_sample_service),
    ) -> Sample:
        request = GetSampleRequest(sample_id=sample_id, access_token=access_token)
        handler = GetSampleHandler(request, service)
        response = await handler.handle()
        return response

    @staticmethod
    async def list_patient_samples(
        subject_id: int = Query(..., gt=0, description="Patient id"),
        _: AccessToken = Depends(
            restrict((Role.ADMIN, Role.LAB_SCIENTIST, Role.DOCTOR))
        ),
        pagination: PaginationParams = Depends(get_pagination_params),
        service: SampleService = Depends(provide_sample_service),
    ) -> list[Sample]:
        handler = ListPatientSamplesHandler(
            subject_id=subject_id,
            limit=pagination.limit,
            offset=pagination.offset,
            sample_service=service,
        )
        response = await handler.handle()
        return response

    @staticmethod
    async def delete(
        sample_id: int,
        access_token: AccessToken = Depends(restrict((Role.ADMIN, Role.DOCTOR))),
        service: SampleService = Depends(provide_sample_service),
    ) -> str:
        request = DeleteSampleRequest(sample_id=sample_id, access_token=access_token)
        handler = DeleteSampleHandler(request, service)
        await handler.handle()
        return "OK"
