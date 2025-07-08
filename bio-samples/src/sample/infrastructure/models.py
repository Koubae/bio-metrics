from sqlalchemy import Column, Enum, String, JSON, BigInteger

from src.core.infrastructure.database.model import Mapper, TimestampedIdModel
from src.sample.domain.entities import SampleType, Status, Sample


class SampleModel(TimestampedIdModel):
    __tablename__ = "sample"

    subject_id = Column(BigInteger, nullable=False, index=True)
    sample_type = Column(
        Enum(SampleType, name="sample_type_enum"),
        nullable=False,
        default=SampleType.UNKNOWN,
    )
    status = Column(
        Enum(Status, name="sample_type_enum"), nullable=False, default=Status.SUBMITTED
    )
    storage_location = Column(String(255), nullable=False)

    sample_metadata = Column(JSON, nullable=True)


class SampleMapper(Mapper[Sample, SampleModel]):  # pragma: no cover
    @classmethod
    def to_entity(cls, model: SampleModel) -> Sample:
        return Sample(
            id=model.id,
            subject_id=model.subject_id,
            sample_type=SampleType(model.sample_type),
            status=Status(model.status),
            storage_location=model.storage_location,
            sample_metadata=model.sample_metadata,
            created=model.created,
            updated=model.updated,
        )

    @classmethod
    def to_model(cls, entity: Sample) -> SampleModel:
        return SampleModel(
            id=entity.id,
            subject_id=entity.subject_id,
            sample_type=SampleType(entity.sample_type),
            status=Status(entity.status),
            storage_location=entity.storage_location,
            metadata=entity.sample_metadata,
            created=entity.created,
            updated=entity.updated,
        )
