from fastapi import APIRouter
from app.api.auth import reg, login, logout, active_user

router = APIRouter()

router.include_router(reg.router)
router.include_router(login.router)
router.include_router(logout.router)
router.include_router(active_user.router)
