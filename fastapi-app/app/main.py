from fastapi import FastAPI

from app.api.v1.events import router as events_router
from app.api.v1.health import router as health_router

app = FastAPI(title="FastAPI App")

app.include_router(health_router, prefix="/api/v1")
app.include_router(events_router, prefix="/api/v1")
