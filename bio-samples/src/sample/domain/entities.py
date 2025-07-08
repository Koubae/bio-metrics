from dataclasses import dataclass, field
from enum import StrEnum

from src.core.domain.models import EntityTimestampedIdBase


class SampleType(StrEnum):
    UNKNOWN = "unknown"
    BLOOD = "blood"
    SALIVA = "saliva"
    TISSUE = "tissue"


class Status(StrEnum):
    SUBMITTED = "submitted"
    COLLECTED = "collected"
    PROCESSING = "processing"
    ARCHIVED = "archived"


@dataclass
class Sample(EntityTimestampedIdBase):
    id: int | None
    subject_id: int
    sample_type: SampleType
    status: Status
    storage_location: str

    sample_metadata: dict = field(default_factory=dict)
