from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer(text="Assalomu aleykum, Turist botga qush kelibsiz")
    await state.clear()


@router.message(F.location)
async def get_user_location_handler(message: types.Message):
    lat, long = message.location.latitude, message.location.longitude
    await message.answer(f"{lat} - {long}")

