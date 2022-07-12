from fastapi import APIRouter

router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)


@router.post("/login")
async def login():
    return {"message": "login"}


@router.post("/logout")
async def logout():
    return {"message": "logout"}