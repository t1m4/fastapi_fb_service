from typing import Dict, List

import sqlalchemy as sa
from sqlalchemy.orm import Session

from app import db
from app.campaign import models, tables
from app.types import StrDict


def insert_campaigns(session: Session, campaigns: List[StrDict]) -> List[models.Campaign]:
    db_campaigns = [tables.Campaign(**campaign) for campaign in campaigns]
    session.bulk_save_objects(db_campaigns, return_defaults=True)
    session.commit()
    db_campaign_ids = [campaign.id for campaign in db_campaigns]
    return select_campaigns(db_campaign_ids)  # type: ignore


def update_campaigns(session: Session, campaigns: List[StrDict]):
    session.bulk_update_mappings(tables.Campaign, campaigns)
    session.commit()


def select_campaigns(ids: List[int] | None = None) -> List[models.Campaign]:
    filters = []
    if ids is not None:
        filters.append(tables.Campaign.id.in_(ids))
    query = sa.select(tables.Campaign).where(*filters)
    rows = db.session_select_all(query)
    return [models.Campaign.from_orm(row) for row in rows]


def select_campaigns_as_dict(ids: List[int] | None = None) -> Dict[int, models.Campaign]:
    filters = []
    if ids is not None:
        filters.append(tables.Campaign.id.in_(ids))
    query = sa.select(tables.Campaign).where(*filters)
    rows = db.session_select_all(query)
    return {row.id: models.Campaign.from_orm(row) for row in rows}
