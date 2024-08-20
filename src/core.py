import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.bot import bot_configurations
from src.bot.app import startup_client_bot, shutdown_client_bot
from src.db import db_helper
from src.apps.admin.admin_conf import AdminAuth, UserAdmin, HistoricalPlaceAdmin
from src.logging_conf import setup_logger
from sqladmin import Admin

from src.settings import settings

APP_ROOT = Path(__file__).parent
setup_logger()

logger = logging.getLogger('fastapi_app')

client_bot, client_webhook_url, client_webhook_path, client_dp = bot_configurations(
    settings.bot.BOT_TOKEN, 'client_bot'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await startup_client_bot(client_bot, client_webhook_url, client_dp)
    yield
    # shutdown
    await shutdown_client_bot(client_bot, client_dp)
    await db_helper.dispose()


def mount_folders(app: FastAPI):
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )
    app.mount("/media", StaticFiles(directory=APP_ROOT / "media"), name="media")


def register_admin_models(app: FastAPI):
    authentication_backend = AdminAuth(secret_key=settings.token.secret_key)
    admin = Admin(app=app, engine=db_helper.engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(HistoricalPlaceAdmin)


def create_app() -> FastAPI:
    logger.debug("Creating app...")
    app = FastAPI(
        title="Guid Bot API",
        version="1.0.0",
        default_response_class=ORJSONResponse,
        lifespan=lifespan
    )

    logger.debug("Mount folders...")
    mount_folders(app)

    logger.debug("Configure middleware...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_admin_models(app)

    return app
