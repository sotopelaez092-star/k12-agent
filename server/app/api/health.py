from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone
from ..settings import settings

router = APIRouter(tags=["system"])

@router.get("/health")
def health():
    return {"status": "ok"}

class ReadyOut(BaseModel):
    ready: bool

@router.get("/ready", response_model=ReadyOut, summary="Readiness")
def ready():
    return {"ready": True}

class InfoOut(BaseModel):
    app_name: str
    version: str
    env: str
    startup_time: str

@router.get("/info", response_model=InfoOut, summary="Service Info")
def info():
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "env": settings.env,
        "startup_time": STARTUP_TIME,
    }

class ValidateIn(BaseModel):
    name: str
    age: int

@router.post("/validate", summary="Validation example")
def validate(payload: ValidateIn):
    # 校验成功则返回简单确认；校验失败将由 FastAPI 抛出 RequestValidationError (422)
    return {"ok": True}