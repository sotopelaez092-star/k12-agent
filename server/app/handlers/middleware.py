import logging
import time
import uuid
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_idlogger = logging.getLogger("request")
        start = time.perf_counter()
        logger.info(f"start {request,method} {request.url.path} rid={request_id}")
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start * 1000)
        response.headers["X-Request-ID"]=request_idlogger.info(
            f"end   {request.method} {request.url.path} rid={request_id} "
            f"{duration_ms:.2f}ms status={response.status_code}"
        )
        return response

def register_middlewares(app: FastAPI):
    app.add_middleware(RequestIDMiddleware)