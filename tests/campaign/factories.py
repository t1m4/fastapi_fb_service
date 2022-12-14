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
        with db.create_session() as session:
            campaign = tables.Campaign(**instance.dict())
            session.add(campaign)
            session.commit()
            return models.Campaign.from_orm(campaign)

    @classmethod
    def get(cls, campaign_id: int) -> models.Campaign | None:
        with db.create_session():
            row = db.session_get(tables.Campaign, campaign_id)
        return models.Campaign.from_orm(row) if row else None
