import logging

from fastapi import HTTPException
from pydantic import BaseModel, Field

from src.auth.domain.entities import AccessToken
from src.core.domain.exceptions import (
    UNEXPECTED_ERROR_MESSAGE,
    RepositoryCreateException,
    RepositoryDatabaseConnectionError,
    RepositoryDuplicateRowException,
    RepositoryEntityNotFound,
)
from src.sample.application.sample_service import SampleService
from src.sample.domain.entities import SampleType, Status, Sample

logger = logging.getLogger(__name__)


class CreateSampleRequest(BaseModel):
    subject_id: int = Field(..., ge=1)
    sample_type: SampleType | None = Field(..., description="Sample Type")
    status: Status | None = Field(Status.SUBMITTED, description="Sample Status")
    storage_location: str = Field(..., min_length=3, max_length=255)
    sample_metadata: dict = Field(dict, description="Sample Metadata")


class CreateSampleHandler:
    def __init__(self, request: CreateSampleRequest, sample_service: SampleService):
        self.request: CreateSampleRequest = request
        self.sample_service: SampleService = sample_service

    async def handle(self) -> Sample:
        try:
            sample: Sample = await self.sample_service.create_sample(
                self.request.subject_id,
                self.request.sample_type,
                self.request.status,
                self.request.storage_location,
                self.request.sample_metadata,
            )
        except RepositoryDuplicateRowException as error:
            logger.warning(
                f"Create Sample failed, duplicate sample {CreateSampleRequest} : {repr(error)}",
                extra={"extra": {"sample": CreateSampleRequest}},
            )
            raise HTTPException(
                status_code=409,
                detail={"error": f"Sample '{CreateSampleRequest}' already exists!"},
            )

        except (RepositoryCreateException, RepositoryDatabaseConnectionError) as error:
            logger.exception(
                f"Create Sample failed, Unexpected exception, sample {CreateSampleRequest} : {repr(error)}",
                extra={"extra": {"sample": CreateSampleRequest}},
            )
            raise HTTPException(
                status_code=500, detail={"error": UNEXPECTED_ERROR_MESSAGE}
            )

        return sample


class GetSampleRequest(BaseModel):
    sample_id: int = Field(..., gt=0)
    access_token: AccessToken = Field(...)


class GetSampleHandler:
    def __init__(self, request: GetSampleRequest, sample_service: SampleService):
        self.request: GetSampleRequest = request
        self.sample_service: SampleService = sample_service

    async def handle(self) -> Sample:
        sample_id = self.request.sample_id
        try:
            sample = await self.sample_service.get(sample_id)
        except RepositoryEntityNotFound as error:
            logger.info(
                f"Get Sample Failed, Sample {sample_id} not found: {repr(error)}",
                extra={"extra": {"sample_id": sample_id}},
            )
            raise HTTPException(
                status_code=404,
                detail={"error": f"Sample '{sample_id}' does not exists!"},
            )
        return sample


class ListPatientSamplesHandler:
    def __init__(
        self, subject_id: int, limit: int, offset: int, sample_service: SampleService
    ):
        self.subject_id: int = subject_id
        self.limit: int = limit
        self.offset: int = offset
        self.sample_service: SampleService = sample_service

    async def handle(self) -> list[Sample]:
        accounts = await self.sample_service.get_patient_samples(
            self.subject_id, self.limit, self.offset
        )
        return accounts


class DeleteSampleRequest(BaseModel):
    sample_id: int = Field(..., gt=1)
    access_token: AccessToken = Field(...)


class DeleteSampleHandler:
    def __init__(self, request: DeleteSampleRequest, sample_service: SampleService):
        self.request: DeleteSampleRequest = request
        self.sample_service: SampleService = sample_service

    async def handle(self) -> bool:
        sample_id = self.request.sample_id
        try:
            await self.sample_service.get(sample_id)
        except RepositoryEntityNotFound as error:
            logger.info(
                f"Get Sample Failed, Sample {sample_id} not found: {repr(error)}",
                extra={"extra": {"sample_id": sample_id}},
            )
            raise HTTPException(
                status_code=404,
                detail={"error": f"Sample '{sample_id}' does not exists!"},
            )
        await self.sample_service.delete(sample_id)
        return True
