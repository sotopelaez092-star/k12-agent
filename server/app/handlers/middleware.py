import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from ..settings import settings


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        logger = logging.getLogger("request")
        start = time.perf_counter()
        logger.info(
            "request_start",
            extra={
                "method": request.method,
                "path": request.url.path,
                "rid": request_id,
            },
        )
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            status_code = 500
            duration_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "request_end",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "rid": request_id,
                    "duration_ms": duration_ms,
                    "status": status_code,
                },
            )
            raise
        else:
            duration_ms = (time.perf_counter() - start) * 1000
            response.headers["X-Request-ID"] = request_id
            logger.info(
                "request_end",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "rid": request_id,
                    "duration_ms": duration_ms,
                    "status": status_code,
                },
            )
            return response


def register_middlewares(app: FastAPI):
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
        expose_headers=settings.cors_expose_headers,
        allow_credentials=settings.cors_allow_credentials,
    )
