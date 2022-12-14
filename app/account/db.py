from typing import List

import sqlalchemy
from sqlalchemy.orm import Session

from app import db
from app.account import models, tables
from app.campaign import tables as campaign_tables


def insert_account(session: Session, account: models.CreateAccount) -> models.Account:
    db_account = tables.Account(**account.dict())
    session.add(db_account)
    session.commit()
    return models.Account.from_orm(db_account)


def select_account(id_: int) -> models.Account | None:
    db_account = db.session_get(tables.Account, id_)
    return models.Account.from_orm(db_account)


def select_accounts(company_id: int | None = None, ids: List[int] | None = None) -> List[models.Account]:
    filters = []
    if company_id is not None:
        filters.append(tables.Account.company_id == company_id)
    if ids is not None:
        filters.append(tables.Account.id.in_(ids))
    query = sqlalchemy.select(tables.Account).where(*filters)
    return [models.Account.from_orm(account) for account in db.session_select_all(query)]


def select_accounts_by_campaigns(campaign_ids: List[int]) -> List[models.Account]:
    query = (
        sqlalchemy.select(tables.Account)
        .join(campaign_tables.Campaign)
        .where(campaign_tables.Campaign.id.in_(campaign_ids))
    )
    return db.session_select_all(query)
