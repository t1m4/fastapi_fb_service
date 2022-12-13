from app import db
from app.account import services
from tests.account.factories import AccountFactory


def test_get_account():
    account = AccountFactory.create()
    with db.connect():
        db_account = services.get_account(account.id)
        assert account == db_account


def test_get_accounts():
    account_1 = AccountFactory.create(name="test1")
    AccountFactory.create(name="test2", company_id=account_1.company_id)
    with db.connect():
        db_accounts = services.get_accounts(account_1.company_id)
        assert len(db_accounts) == 2
