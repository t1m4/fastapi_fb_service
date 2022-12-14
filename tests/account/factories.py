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
        with db.create_session() as session:
            account = tables.Account(**instance.dict())
            session.add(account)
            session.commit()
            return models.Account.from_orm(account)

    @classmethod
    def get(cls, id_: int) -> models.Account | None:
        with db.create_session():
            row = db.session_get(tables.Account, id_)
        return models.Account.from_orm(row) if row else None
