from src.sample.domain.entities import SampleType, Sample, Status
from src.sample.domain.ports import SampleRepository


class SampleService:
    def __init__(self, sample_repository: SampleRepository) -> None:
        self.sample_repository: SampleRepository = sample_repository

    async def create_sample(
        self,
        subject_id: int,
        sample_type: SampleType,
        status: Status,
        storage_location: str,
        sample_metadata: dict,
    ) -> Sample:
        entity = Sample(
            id=None,
            subject_id=subject_id,
            sample_type=sample_type,
            status=status,
            storage_location=storage_location,
            sample_metadata=sample_metadata,
        )
        await self.sample_repository.create(entity)
        return entity

    async def get(self, sample_id: int) -> Sample | None:
        account = await self.sample_repository.find_by_pk(sample_id)
        return account

    async def get_patient_samples(
        self, subject_id: int, limit: int = 10, offset: int = 0
    ) -> list[Sample]:
        return await self.sample_repository.list_samples_by_subject_id(
            subject_id, limit, offset
        )

    async def delete(self, sample_id: int) -> None:
        await self.sample_repository.delete_by_pk(sample_id)
