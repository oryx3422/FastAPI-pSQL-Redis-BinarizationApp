from fastapi import APIRouter, HTTPException, Response
from authx import AuthX
from sqlalchemy import select

from app.core.config import config
from app.models.user import UserModel
from app.db.session import SessionDep
from app.schemas.user import UserLoginSchema
from app.services.auth import verify_password


router = APIRouter()
security = AuthX(config=config)


@router.post("/login", tags=["authz/auth"])
async def login(creds: UserLoginSchema, response: Response, session: SessionDep):
    query = select(UserModel).where(UserModel.email == creds.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token}
