from fastapi import APIRouter, Response
from app.core.config import config

router = APIRouter()

@router.post("/logout", tags=["authz/auth"])
async def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"ok": True, "message": "Successfully logged out"}
