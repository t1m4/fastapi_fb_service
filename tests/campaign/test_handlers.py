from http import HTTPStatus

import pytest

from app.campaign.handlers import router
from app.config import config
from tests.account.factories import AccountFactory
from tests.campaign.factories import CampaignFactory


@pytest.mark.parametrize(
    "campaigns",
    [
        [{"name": "test_1"}],
        [{"name": "test_1"}, {"name": "test_2"}],
        [{"name": "test_1"}, {"name": "test_2"}, {"name": "test_3"}],
    ],
)
def test_create_campaigns(client, campaigns):
    account = AccountFactory.create()
    for campaign in campaigns:
        campaign["credential_id"] = account.id
    url = config.BASE_API_PATH + router.url_path_for("create_campaigns")

    response = client.post(url, json=campaigns)
    assert response.status_code == HTTPStatus.OK
    response_campaigns = response.json()
    assert isinstance(response_campaigns, list)
    assert len(response_campaigns) == len(campaigns)
    for index, campaign in enumerate(response_campaigns):
        expected_campaign = campaigns[index]
        for field, value in expected_campaign.items():
            assert value == campaign.get(field), "Error with {}".format(field)
        assert isinstance(campaign.get("id"), int)

        db_campaign = CampaignFactory.get(campaign["id"])
        json_db_campaign = db_campaign.dict()  # type: ignore
        for field, value in expected_campaign.items():
            assert value == json_db_campaign.get(field)


@pytest.mark.parametrize(
    "campaigns",
    [
        [{"name": "test_1"}],
        [{"name": "test_1"}, {"name": "test_2"}],
        [{"name": "test_1"}, {"name": "test_2"}, {"name": "test_3"}],
    ],
)
def test_update_campaigns(client, campaigns):
    account = AccountFactory.create()
    for campaign in campaigns:
        created_campaign = CampaignFactory.create(credential_id=account.id)
        campaign["id"] = created_campaign.id
    url = config.BASE_API_PATH + router.url_path_for("update_campaigns")
    response = client.put(url, json=campaigns)
    assert response.status_code == HTTPStatus.OK

    response_campaigns = response.json()
    assert isinstance(response_campaigns, list)
    assert len(response_campaigns) == len(campaigns)
    for index, campaign in enumerate(response_campaigns):
        expected_campaign = campaigns[index]
        for field, value in expected_campaign.items():
            assert value == campaign.get(field), "Error with {}".format(field)
        assert isinstance(campaign.get("id"), int)

        db_campaign = CampaignFactory.get(campaign["id"])
        json_db_campaign = db_campaign.dict()  # type: ignore
        for field, value in expected_campaign.items():
            assert value == json_db_campaign.get(field)
