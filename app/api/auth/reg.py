from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.services.auth import hash_password
from app.models.user import UserModel
from app.db.session import SessionDep
from app.schemas.user import UserAddSchema

router = APIRouter()

@router.post("/reg", tags=["authz/auth"])
async def create_user(user: UserAddSchema, session: SessionDep):
    query = select(UserModel).where(UserModel.email == user.email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)
    new_user = UserModel(email=user.email, password=hashed_pw)
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return {"ok": True, "id": new_user.id}
