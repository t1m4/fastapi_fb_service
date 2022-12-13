from typing import List

from app.account import db, models
from app.errors import DoesNotExistsError


def get_account(id_: int) -> models.Account:
    account = db.select_account(id_)
    if not account:
        raise DoesNotExistsError("Account doesn't exists")
    return account


def get_accounts(company_id: int) -> List[models.Account]:
    return db.select_accounts(company_id)
