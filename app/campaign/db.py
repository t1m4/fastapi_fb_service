from typing import Dict, List

import sqlalchemy as sa

from app import db
from app.campaign import models, tables
from app.types import StrDict


def insert_campaigns(campaigns: List[StrDict]) -> List[models.Campaign]:
    query = sa.insert(tables.Campaign).values(campaigns).returning(tables.Campaign)
    rows = db.select_all(query)

    return [models.Campaign.from_orm(row) for row in rows]


def update_campaigns(campaigns: List[StrDict]):
    campaign_values = {}
    for field in campaigns[0].keys():
        if field != "campaign_id":
            campaign_values[field] = sa.bindparam(field)
    query = (
        sa.update(tables.Campaign).where(tables.Campaign.id == sa.bindparam("campaign_id")).values(**campaign_values)
    )
    db.execute(query, campaigns)


def select_campaigns(ids: List[int] | None = None) -> List[models.Campaign]:
    filters = []
    if ids is not None:
        filters.append(tables.Campaign.id.in_(ids))
    query = sa.select(tables.Campaign).where(*filters)
    rows = db.select_all(query)
    return [models.Campaign.from_orm(row) for row in rows]


def select_campaigns_as_dict(ids: List[int] | None = None) -> Dict[int, models.Campaign]:
    filters = []
    if ids is not None:
        filters.append(tables.Campaign.id.in_(ids))
    query = sa.select(tables.Campaign).where(*filters)
    rows = db.select_all(query)
    return {row["id"]: models.Campaign.from_orm(row) for row in rows}
