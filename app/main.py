from fastapi import FastAPI
from app.api.routes import router as douyin_router

app = FastAPI(title="Douyin Crawler API")

app.include_router(douyin_router, prefix="/api", tags=[""])
