from typing import List

from pydantic import BaseModel, Field


class BaseCampaign(BaseModel):
    credential_id: int
    name: str


class CampaignCreate(BaseCampaign):
    ...


class CampaignUpdate(BaseModel):
    campaign_id: int = Field(..., alias="id")
    name: str


class CampaignsCreate(BaseModel):
    __root__: List[CampaignCreate]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class CampaignsUpdate(BaseModel):
    __root__: List[CampaignUpdate]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class Campaign(BaseCampaign):
    id: int

    class Config:
        orm_mode = True


class Campaigns(BaseModel):
    __root__: List[Campaign]
