from fastapi import APIRouter

from .disk import router as disk_router
from .auth import router as auth_router

router = APIRouter(prefix="/api")

router.include_router(disk_router)
router.include_router(auth_router)
