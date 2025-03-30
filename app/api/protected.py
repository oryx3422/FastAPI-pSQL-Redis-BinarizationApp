from fastapi import APIRouter, Depends
from authx import AuthX
from app.core.config import config

router = APIRouter()
security = AuthX(config=config)

@router.get("/protected", dependencies=[Depends(security.access_token_required)], tags=["Protected"])
async def protected():
    return {"data": "You are authorized!"}