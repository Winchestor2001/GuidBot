from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from src.settings import settings


def bot_configurations(bot_token: str, path_name: str):
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode='html'))
    webhook_path = f"/bot/{path_name}/{bot_token}"
    webhook_url = settings.run.domain + webhook_path
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    return bot, webhook_url, webhook_path, dp
