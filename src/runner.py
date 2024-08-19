import logging
import uvicorn
from aiogram import types

from src.apps import api_router
from src.core import create_app, client_webhook_path, client_dp, client_bot
from src.settings import settings

logger = logging.getLogger('fastapi_app')

main_app = create_app()

main_app.include_router(api_router)


@main_app.post(client_webhook_path)
async def client_bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await client_dp.feed_update(bot=client_bot, update=telegram_update)



if __name__ == "__main__":
    logger.debug("Application started")
    uvicorn.run(
        "runner:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
    logger.debug("Application stopped")
