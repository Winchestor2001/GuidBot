import logging

from src.bot.handlers import router


async def startup_client_bot(bot, webhook_url, dp):
    await bot.set_webhook(url=webhook_url, drop_pending_updates=True, allowed_updates=['message', 'callback_query'])
    dp.include_router(router)


async def shutdown_client_bot(bot, dp):
    await dp.storage.close()
    await bot.delete_webhook(drop_pending_updates=True)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
