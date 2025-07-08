from abc import ABC, abstractmethod

from src.core.domain.ports import AsyncRepository
from src.core.domain.types import Model
from src.sample.domain.entities import Sample


class SampleRepository(AsyncRepository[Sample, Model], ABC):
    @abstractmethod
    async def list_samples_by_subject_id(
        self, subject_id: int, limit: int, offset: int
    ) -> list[Sample]: ...
