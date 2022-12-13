import sqlalchemy as sa
from pydantic_factories import ModelFactory

from app import db
from app.campaign import models, tables


class CampaignFactory(ModelFactory[models.Campaign]):
    __model__ = models.Campaign

    @classmethod
    def create(cls, **kwargs) -> models.Campaign:
        instance = cls.build(**kwargs)
        return cls.save(instance)

    @staticmethod
    def save(instance: models.Campaign) -> models.Campaign:
        with db.begin():
            query = sa.insert(tables.Campaign).values(instance.dict()).returning(tables.Campaign)
            row = db.select_one(query)
            return models.Campaign.from_orm(row)

    @classmethod
    def get(cls, campaign_id: int) -> models.Campaign | None:
        with db.connect():
            row = db.select_one(sa.select(tables.Campaign).where(tables.Campaign.id == campaign_id))
        return models.Campaign.from_orm(row) if row else None
