# 模块：应用初始化与路由注册
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.health import router as system_router
from .api.metrics import router as metrics_router
from .handlers.errors import register_error_handlers
from .handlers.middleware import register_middlewares
from .logging import setup_logging
from .settings import settings

setup_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动（可在此初始化资源，如DB连接、缓存等）
    yield
    # 应用停止（清理资源、flush指标等）


app = FastAPI(lifespan=lifespan)

app.include_router(system_router)
app.include_router(metrics_router)
register_error_handlers(app)
register_middlewares(app)
