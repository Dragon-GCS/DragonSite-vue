from sys import prefix
from fastapi import APIRouter
from fastapp.api import disk

router = APIRouter(
    prefix='/api',
    tags=['api'],
)
router.include_router(disk.router)
