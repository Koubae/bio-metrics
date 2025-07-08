from abc import ABC
from dataclasses import is_dataclass
from typing import Any, Generic

import sqlalchemy
from sqlalchemy import ColumnElement, and_, inspect, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.exceptions import (
    RepositoryCreateException,
    RepositoryDatabaseConnectionError,
    RepositoryDuplicateRowException,
    RepositoryPKMissingException,
)
from src.core.domain.ports import AsyncRepository
from src.core.domain.types import DBPrimaryKey, Entity
from src.core.infrastructure.database.model import DbModel, Mapper


class AsyncSqlalchemyRepository(AsyncRepository, ABC, Generic[Entity, DbModel]):
    _entity: type[Entity]
    _model: type[DbModel]
    _mapper: type[Mapper]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_pk(self, pk: DBPrimaryKey) -> Entity | None:
        model = await self._find_by_pk(pk)
        if model is None:
            return None
        return self._mapper.to_entity(model)

    async def _find_by_pk(self, pk: DBPrimaryKey) -> DbModel | None:
        if isinstance(pk, (str, int)):
            pk = {"id": pk}

        pk_dict: Any = pk
        self._pk_where_clause_from_dict(pk_dict)
        row = await self._session.get(self._model, pk)
        if not row:
            return None
        return row

    async def create(self, entity: Entity) -> None:
        model = self._model(**self._mapper.to_dict(entity))
        await self._create(entity, model)

    async def update(self, entity: Entity) -> bool:
        where = self._pk_where_clause_from_entity(entity)
        stmt = update(self._model).where(where).values(**self._mapper.to_dict_for_update(entity))
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount == 1

    async def delete_by_pk(self, pk: DBPrimaryKey) -> bool:
        model = await self._find_by_pk(pk)
        if model is None:
            return False

        await self._session.delete(model)
        await self._session.flush()
        return True

    def _pk_columns(self) -> Any:
        return inspect(self._model).primary_key

    def _pk_where_clause_from_entity(self, entity: Entity) -> ColumnElement[bool]:
        if not is_dataclass(self._entity):
            raise TypeError("entity_obj must be a dataclass instance")

        data = self._mapper.to_dict(entity)
        return self._pk_where_clause_from_dict(data)

    def _pk_where_clause_from_dict(self, data: dict) -> ColumnElement[bool]:
        cols = self._pk_columns()
        try:
            return and_(*(c == data[c.key] for c in cols))
        except KeyError as err:
            missing = err.args[0]
            raise RepositoryPKMissingException(model=self._model, missing=missing) from None

    async def _create(self, entity, model) -> None:
        try:
            self._session.add(model)
            await self._session.commit()
            await self._session.refresh(model)
        except IntegrityError as error:
            if self._is_duplicate_exception(error):
                raise RepositoryDuplicateRowException(
                    model=self._model,
                    entity=entity,
                    error=f"Duplicate record: {repr(error)}",
                ) from error

            raise RepositoryCreateException(model=self._model, entity=entity, error=repr(error)) from error
        except sqlalchemy.exc.DatabaseError as error:
            raise RepositoryDatabaseConnectionError(model=self._model, entity=entity, error=repr(error)) from error

        if hasattr(entity, "set_id"):
            entity.set_id(model.id)

    @staticmethod
    def _is_duplicate_exception(error: IntegrityError) -> bool:
        error_msg = str(error.orig).lower()
        return any(keyword in error_msg for keyword in ["unique", "duplicate", "already exists"])
