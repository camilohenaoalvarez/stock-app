import os
import time

from fastapi import FastAPI

from app.infrastructure.routes import router
from app.infrastructure.configurations import Config
from app.infrastructure.repositories import Stock


def create_app() -> FastAPI:
    """App creation with a router and a lifespan"""

    async def lifespan(app: FastAPI):
        """Setting up the db client and de DB creation"""
        conf = Config.from_environ(os.environ)
        db_client = Stock.from_config(conf)
        app.state.db_client = db_client

        db_client.init_db()
        yield
        db_client._engine.dispose()

    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app
