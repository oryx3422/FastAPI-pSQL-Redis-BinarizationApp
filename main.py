from fastapi import FastAPI
import uvicorn

from authx import AuthX

from app.core.config import config

from app.api.auth.router import router as auth_router
from app.api.binar import router as binar_router
from app.api.protected import router as protected_router


security = AuthX(config=config)

app = FastAPI()

app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(binar_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8031, reload=True)
