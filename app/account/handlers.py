from fastapi import APIRouter, Path

from app import db
from app.account import models, services

router = APIRouter()


@router.post("/account")
def create_account():
    ...


@router.get("/account")
def get_accounts():
    return {}
    ...


@router.get("/account/{id}", response_model=models.Account)
def get_account(id_: int = Path(..., alias="id")):
    with db.create_session():
        return services.get_account(id_)


@router.put("/account/{id}")
def update_account():
    ...
