from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["system"])

@router.get("/health")
def health():
    return {"status": "ok"}

class ReadyOut(BaseModel):
    ready: bool

@router.get("/ready", response_model=ReadyOut, summary="Readiness")
def ready():
    return {"ready": True}