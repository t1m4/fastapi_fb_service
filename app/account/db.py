from typing import List

import sqlalchemy

from app import db
from app.account import models, tables
from app.campaign import tables as campaign_tables


def insert_account(account: models.CreateAccount) -> models.Account:
    query = (
        sqlalchemy.insert(tables.Account)
        .values(
            account_id=account.account_id,
            company_id=account.company_id,
            name=account.name,
            businesses=account.businesses,
        )
        .returning(tables.Account)
    )
    row = db.select_one(query)
    return models.Account.from_orm(row)


def select_account(id_: int) -> models.Account | None:
    query = sqlalchemy.select(tables.Account).where(tables.Account.id == id_)
    row = db.select_one(query)
    return models.Account.from_orm(row) if row else None


def select_accounts(company_id: int | None = None, ids: List[int] | None = None) -> List[models.Account]:
    filters = []
    if company_id is not None:
        filters.append(tables.Account.company_id == company_id)
    if ids is not None:
        filters.append(tables.Account.id.in_(ids))
    query = sqlalchemy.select(tables.Account).where(*filters)
    rows = db.select_all(query)
    return [models.Account.from_orm(row) for row in rows]


def select_accounts_by_campaigns(campaign_ids: List[int]) -> List[models.Account]:
    query = (
        sqlalchemy.select(tables.Account)
        .join(campaign_tables.Campaign)
        .where(campaign_tables.Campaign.id.in_(campaign_ids))
    )
    rows = db.select_all(query)
    return [models.Account.from_orm(row) for row in rows]


def update_account(id_: int, account: models.UpdateAccount) -> models.Account | None:
    query = (
        sqlalchemy.update(tables.Account)
        .values(**account.dict())
        .where(tables.Account.id == id_)
        .returning(tables.Account)
    )
    row = db.select_one(query)
    return models.Account.from_orm(row) if row else None
