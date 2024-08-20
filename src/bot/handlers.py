from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging

from src.bot.utils import make_context_text
from src.db.crud import create_user_obj, search_places_obj

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    await create_user_obj(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer(text="Assalomu aleykum, Turist botga qush kelibsiz")
    await state.clear()


@router.message(F.location)
async def get_user_location_handler(message: types.Message):
    lat, long = message.location.latitude, message.location.longitude
    places = await search_places_obj(lat, long)
    context = await make_context_text(places)
    await message.answer(f"{lat} - {long}")
    await message.answer(context)

