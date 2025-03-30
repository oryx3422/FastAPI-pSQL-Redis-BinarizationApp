from fastapi import APIRouter, Depends, HTTPException
from authx import AuthX
from app.core.config import config

from app.services.binar import bradley_threshold
from app.schemas.binar import ImageBase64

router = APIRouter()
security = AuthX(config=config)


# Бинаризация изображения
@router.post("/binary_image", dependencies=[Depends(security.access_token_required)], tags=["Protected"])
async def binary_image(image_data: ImageBase64):
    try:
        result_base64 = bradley_threshold(image_data.image_base64)
        return {"result_image_base64": result_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
