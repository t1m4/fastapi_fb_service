from fastapi import APIRouter

router = APIRouter()


@router.post("/account")
def create_account():
    ...


@router.get("/account")
def get_accounts():
    return {}
    ...


@router.get("/account/{id}")
def get_account():
    ...


@router.put("/account/{id}")
def update_account():
    ...
