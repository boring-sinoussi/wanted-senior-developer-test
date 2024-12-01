import logging.config

from fastapi import FastAPI

from app.route import router
from app.core.connection import db
from app.core.logging.config import LOGGING
from app.core.settings import get_settings

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        routes=router.routes,
        docs_url=None,
        redoc_url="/docs",
        env=settings.APP_ENV,
    )

    # Databases
    app.add_event_handler("startup", db.check_connection)
    app.add_event_handler("shutdown", db.dispose_connection)

    # Logging
    logging.config.dictConfig(LOGGING)

    return app
