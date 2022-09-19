from fastapi import APIRouter

from .auth import router as auth_router
from .disk import router as disk_router

router = APIRouter(prefix="/api")

router.include_router(disk_router)
router.include_router(auth_router)
