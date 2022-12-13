import sqlalchemy as sa
from pydantic_factories import ModelFactory

from app import db
from app.account import models, tables


class AccountFactory(ModelFactory[models.Account]):
    __model__ = models.Account

    @classmethod
    def create(cls, **kwargs) -> models.Account:
        instance = cls.build(**kwargs)
        return cls.save(instance)

    @staticmethod
    def save(instance: models.Account) -> models.Account:
        with db.begin():
            query = sa.insert(tables.Account).values(instance.dict()).returning(tables.Account)
            row = db.select_one(query)
            return models.Account.from_orm(row)

    @classmethod
    def get(cls, id_: int) -> models.Account | None:
        with db.connect():
            row = db.select_one(sa.select(tables.Account).where(tables.Account.id == id_))
        return models.Account.from_orm(row) if row else None
