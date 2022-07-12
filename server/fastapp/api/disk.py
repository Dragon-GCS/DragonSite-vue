from fastapi import APIRouter

router = APIRouter(
    prefix='/disk',
    tags=['disk'],
)

@router.get("/")
async def get_disk_content():
    return {"message": "get disk content"}