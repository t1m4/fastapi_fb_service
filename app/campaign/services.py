from typing import List

from sqlalchemy.orm import Session

from app.account import db as account_db
from app.account import models as account_models
from app.campaign import db, models, validation


class CreateCampaignsService:
    def __init__(self, session: Session, campaigns: models.CampaignsCreate) -> None:
        self.session = session
        self.campaigns = campaigns
        account_ids: List[int] = [campaign.credential_id for campaign in self.campaigns]
        self.accounts: List[account_models.Account] = account_db.select_accounts(ids=account_ids)
        self.validation = validation.CampaignsCreateValidation(self.campaigns, self.accounts)

    def create(self) -> List[models.Campaign]:
        self.validation.validate()
        campaigns = [campaign.dict() for campaign in self.campaigns]
        return db.insert_campaigns(self.session, campaigns)


class UpdateCampaignsService:
    def __init__(self, session: Session, campaigns: models.CampaignsUpdate) -> None:
        self.session = session
        self.campaigns = campaigns
        self.campaign_ids: List[int] = [campaign.id for campaign in self.campaigns]
        accounts: List[account_models.Account] = account_db.select_accounts_by_campaigns(self.campaign_ids)
        db_campaigns_dict = db.select_campaigns_as_dict(ids=self.campaign_ids)
        self.validation = validation.CampaignsUpdateValidation(self.campaigns, accounts, db_campaigns_dict)

    def update(self) -> List[models.Campaign]:
        self.validation.validate()
        campaigns = [campaign.dict() for campaign in self.campaigns]
        db.update_campaigns(self.session, campaigns)
        return db.select_campaigns(ids=self.campaign_ids)
