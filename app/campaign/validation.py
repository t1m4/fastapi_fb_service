from typing import Dict, List

from app.account import models as account_models
from app.campaign import models
from app.errors import BaseError


class CampaignValidation:
    def validate(
        self, validated_data: models.CampaignCreate | models.CampaignUpdate, instance: models.Campaign | None = None
    ):
        ...


class CampaignsCreateValidation:
    def __init__(self, campaigns: models.CampaignsCreate, accounts: List[account_models.Account]) -> None:
        """
        Args:
            campaigns (CampaignsCreate): All campaigns
            accounts (List[Account]): All accounts from given campaigns
        """
        self.campaigns = campaigns
        self.accounts = accounts

    def _validate_accounts(self):
        """
        Raises:
            BaseError: raises when account with given id doesn't exists
        """
        errors = []
        db_account_ids: List[int] = [credential.id for credential in self.accounts]
        for index, campaign in enumerate(self.campaigns):
            if campaign.credential_id not in db_account_ids:
                errors.append({index: "Account with id {} doesn't exists".format(campaign.credential_id)})
        if any(errors):
            raise BaseError(errors)

    def validate(self):
        """
        Raises:
            BaseError: raises any campaign don't pass validation
        """
        self._validate_accounts()
        errors = []
        for index, campaign in enumerate(self.campaigns):
            validation_service = CampaignValidation()
            try:
                validation_service.validate(campaign)
            except BaseError as exception:
                errors.append({index: exception.message})
        if any(errors):
            raise BaseError(errors)


class CampaignsUpdateValidation:
    def __init__(
        self,
        campaigns: models.CampaignsUpdate,
        accounts: List[account_models.Account],
        db_campaigns: Dict[int, models.Campaign],
    ) -> None:
        """
        Args:
            campaigns (CampaignsCreate): All campaigns
            accounts (List[Account]): All accounts from given campaigns
        """
        self.campaigns = campaigns
        self.db_campaigns = db_campaigns
        self.accounts = accounts

    def _validate_campaign_ids(self):
        """
        Raises:
            BaseError: raises when account with given id doesn't exists
        """
        errors = []
        for index, campaign in enumerate(self.campaigns):
            if campaign.campaign_id not in self.db_campaigns:
                errors.append({index: "Campaign with id {} doesn't exists".format(campaign.campaign_id)})
        if any(errors):
            raise BaseError(errors)

    def validate(self):
        """
        Raises:
            BaseError: raises any campaign don't pass validation
        """
        self._validate_campaign_ids()
        errors = []
        for index, campaign in enumerate(self.campaigns):
            validation_service = CampaignValidation()
            try:
                validation_service.validate(campaign, self.db_campaigns[campaign.campaign_id])
            except BaseError as exception:
                errors.append({index: exception.message})
        if any(errors):
            raise BaseError(errors)
