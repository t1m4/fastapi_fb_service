from typing import List

from pydantic import BaseModel, Field


class BaseAccount(BaseModel):
    account_id: str = Field(..., max_length=50)
    company_id: int
    name: str = Field(..., max_length=100)
    businesses: List[str] = []


class CreateAccount(BaseAccount):
    ...


class UpdateAccount(BaseAccount):
    ...


class Account(BaseAccount):
    id: int

    class Config:
        orm_mode = True
