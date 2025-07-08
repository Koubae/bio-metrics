from abc import ABC
from dataclasses import is_dataclass
from typing import Any, Generic

import sqlalchemy
from sqlalchemy import ColumnElement, and_, inspect, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.types import Entity, DBPrimaryKey
from src.core.domain.ports import AsyncRepository
from src.core.infrastructure.database.model import Mapper, DbModel
from src.core.domain.exceptions import (
    RepositoryCreateException,
    RepositoryPKMissingException,
)


class AsyncSqlalchemyRepository(AsyncRepository, ABC, Generic[Entity, DbModel]):
    _domain: type[Entity]
    _model: type[DbModel]
    _mapper: type[Mapper]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_pk(self, pk: DBPrimaryKey) -> Entity | None:
        model = await self._find_by_pk(pk)
        if model is None:
            return None
        return self._mapper.to_domain(model)

    async def _find_by_pk(self, pk: DBPrimaryKey) -> DbModel | None:
        if isinstance(pk, (str, int)):
            pk = {"id": pk}

        pk_dict: Any = pk
        self._pk_where_clause_from_dict(pk_dict)
        row = await self._session.get(self._model, pk)
        if not row:
            return None
        return row

    async def create(self, domain: Entity) -> None:
        model = self._model(**self._mapper.to_dict(domain))

        try:
            self._session.add(model)
            await self._session.flush()
        except sqlalchemy.exc.IntegrityError as error:
            raise RepositoryCreateException(
                model=self._model, domain=domain, error=repr(error)
            ) from error

        if hasattr(domain, "set_id"):
            domain.set_id(model.id)

    async def update(self, domain: Entity) -> bool:
        where = self._pk_where_clause_from_domain(domain)
        stmt = (
            update(self._model)
            .where(where)
            .values(**self._mapper.to_dict_for_update(domain))
        )
        result = await self._session.execute(stmt)
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

    def _pk_where_clause_from_domain(self, domain: Entity) -> ColumnElement[bool]:
        if not is_dataclass(self._domain):
            raise TypeError("domain_obj must be a dataclass instance")

        data = self._mapper.to_dict(domain)
        return self._pk_where_clause_from_dict(data)

    def _pk_where_clause_from_dict(self, data: dict) -> ColumnElement[bool]:
        cols = self._pk_columns()
        try:
            return and_(*(c == data[c.key] for c in cols))
        except KeyError as err:
            missing = err.args[0]
            raise RepositoryPKMissingException(
                model=self._model, missing=missing
            ) from None
