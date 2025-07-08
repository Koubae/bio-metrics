from dataclasses import asdict
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import ClassVar, Generic, TypeVar

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase

from src.core.domain.types import Entity


class Base(DeclarativeBase):
    pass


class IdModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class AuditModel(Base):
    __abstract__ = True

    created = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
    )


class TimestampedIdModel(IdModel, AuditModel):
    __abstract__ = True


DbModel = TypeVar("DbModel", bound=Base)


class Mapper(ABC, Generic[Entity, DbModel]):
    _domain: type[Entity]
    _model: type[DbModel]
    _remove_values_for_update: ClassVar[set[str]] = {"id", "created", "updated"}
    """Set of fields that should be excluded from update query."""

    @classmethod
    @abstractmethod
    def to_domain(cls, model: DbModel) -> Entity:
        pass

    @classmethod
    def to_model(cls, entity: Entity) -> DbModel:
        return cls._model(**cls.to_dict(entity))

    @classmethod
    def to_dict(cls, domain: Entity) -> dict:
        return asdict(domain)

    @classmethod
    def to_dict_for_update(cls, domain: Entity) -> dict:
        values = cls.to_dict(domain)
        return {
            k: v for k, v in values.items() if k not in cls._remove_values_for_update
        }
