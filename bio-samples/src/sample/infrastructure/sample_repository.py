from sqlalchemy import select

from src.core.infrastructure.database.async_repository import AsyncSqlalchemyRepository
from src.sample.domain.entities import Sample
from src.sample.domain.ports import SampleRepository
from src.sample.infrastructure.models import SampleModel, SampleMapper


class SampleRepositoryAdapter(
    AsyncSqlalchemyRepository[Sample, SampleModel], SampleRepository
):
    _entity: type[Sample] = Sample
    _model: type[SampleModel] = SampleModel
    _mapper: type[SampleMapper] = SampleMapper

    async def list_samples_by_subject_id(self, limit: int, offset: int) -> list[Sample]:
        stmt = select(SampleModel).order_by(SampleModel.id).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        accounts = [self._mapper.to_entity(row) for row in rows]
        return accounts
