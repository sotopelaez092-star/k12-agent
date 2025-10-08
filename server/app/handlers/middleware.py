import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram
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
            REQUEST_COUNT.labels(
                request.method, request.url.path, str(status_code)
            ).inc()
            REQUEST_LATENCY.labels(
                request.method, request.url.path, str(status_code)
            ).observe(duration_ms / 1000.0)
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
            REQUEST_COUNT.labels(
                request.method, request.url.path, str(status_code)
            ).inc()
            REQUEST_LATENCY.labels(
                request.method, request.url.path, str(status_code)
            ).observe(duration_ms / 1000.0)
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


# 请求指标
REQUEST_COUNT = Counter(
    "app_http_requests_total",
    "Total HTTP requests processed",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path", "status"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5],
)
