from fastapi import FastAPI
from .logging import setup_logging
from .settings import settings
from .api.health import router as system_router
from .handlers.errors import register_error_handlers

setup_logging(settings.log_level)
app = FastAPI()

app.include_router(system_router)
register_error_handlers(app)