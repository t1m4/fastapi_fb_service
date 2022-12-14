from fastapi import APIRouter

from app import db
from app.campaign import models, services

router = APIRouter()


@router.post("/campaign/bulk", response_model=models.Campaigns)
def create_campaigns(campaigns: models.CampaignsCreate) -> models.Campaigns:
    with db.begin():
        service = services.CreateCampaignsService(campaigns)
        created_campaigns = service.create()
    return models.Campaigns(__root__=created_campaigns)


@router.put("/campaign/bulk", response_model=models.Campaigns)
def update_campaigns(campaigns: models.CampaignsUpdate) -> models.Campaigns:
    with db.begin():
        service = services.UpdateCampaignsService(campaigns)
        created_campaigns = service.update()
    return models.Campaigns(__root__=created_campaigns)
