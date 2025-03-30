from authx import AuthX, TokenPayload
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from typing import Annotated

from app.models.user import UserModel
from app.db.session import SessionDep
from app.core.config import config

router = APIRouter()
security = AuthX(config=config)

async def get_current_user(
    session: SessionDep,
    token_payload: Annotated[TokenPayload, Depends(security.access_token_required)]
) -> UserModel:
    user_id = token_payload.sub
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/users/me/", tags=["Active user"])
async def show_current_user(current_user: UserModel = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
