from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

def register_error_handlers(app: FastAPI):
    from starlette.exceptions import HTTPException as StarletteHTTPException

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        resp = JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.status_code, "message": str(exc.detail)}},
        )
        rid = getattr(request.state, "request_id", None)
        if rid:
            resp.headers["X-Request-ID"] = rid
        return resp

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        resp = JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.status_code, "message": str(exc.detail)}},
        )
        rid = getattr(request.state, "request_id", None)
        if rid:
            resp.headers["X-Request-ID"] = rid
        return resp

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        resp = JSONResponse(
            status_code=500,
            content={"error": {"code": 500, "message": "Internal Server Error"}},
        )
        rid = getattr(request.state, "request_id", None)
        if rid:
            resp.headers["X-Request-ID"] = rid
        return resp

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        resp = JSONResponse(
            status_code=422,
            content={"error": {"code": 422, "message": "Validation Error", "details": exc.errors()}},
        )
        rid = getattr(request.state, "request_id", None)
        if rid:
            resp.headers["X-Request-ID"] = rid
        return resp