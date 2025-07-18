from sqlalchemy import Column, Enum, String

from src.account.domain.entities import Account, AccountWithPassword
from src.auth.domain.entities import Role
from src.core.infrastructure.database.model import Mapper, TimestampedIdModel


class AccountModel(TimestampedIdModel):
    __tablename__ = "account"

    username = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role, name="role_enum"), nullable=False, default=Role.USER)


class AccountMapper(Mapper[Account, AccountModel]):  # pragma: no cover
    @classmethod
    def to_entity(cls, model: AccountModel) -> Account:
        return Account(
            id=model.id,
            username=model.username,
            role=Role(model.role),
            created=model.created,
            updated=model.updated,
        )

    @classmethod
    def to_entity_with_secret(cls, model: AccountModel) -> AccountWithPassword:
        return AccountWithPassword(
            id=model.id,
            username=model.username,
            role=Role(model.role),
            password=model.password,
        )

    @classmethod
    def to_model(cls, entity: Account) -> AccountModel:
        return AccountModel(id=entity.id, username=entity.username, role=Role(entity.role))
