from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging

from src.bot.keyboards import places_btn, location_btn, cancel_btn, add_place, remove_btn
from src.bot.states import Places, HistoricalPlaces
from src.bot.utils import make_context_text, get_address
from src.db.crud import create_user_obj, search_places_obj, search_places_by_name_obj, user_detail_obj, \
    create_history_place_obj
from src.db.models import UserRole

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    await create_user_obj(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )
    btn = await location_btn()
    await message.answer(text="Assalomu aleykum, Turist botga qush kelibsiz", reply_markup=btn)
    await state.clear()


@router.message(HistoricalPlaces.location, F.location)
async def history_place_location_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lat, long = message.location.latitude, message.location.longitude
    address = await get_address(lat, long)
    await create_history_place_obj(title=data['title'], description=data['description'], latitude=lat,
                                   longitude=long, address=address)
    await message.answer("Joy muvaffaqiyatli qo'shildi ✅", reply_markup=remove_btn)


@router.message(F.location)
async def get_user_location_handler(message: types.Message, state: FSMContext):
    lat, long = message.location.latitude, message.location.longitude
    places = await search_places_obj(lat, long)
    if not places:
        await message.answer("Ma'lumot topilmadi")
        return
    btn = await places_btn(places)
    await message.answer("Yaqin joylar:", reply_markup=btn)
    await state.set_state(Places.place)


@router.message(Places.place)
async def place_detail_handler(message: types.Message, state: FSMContext):
    if message.text == f"🔙 Ortga":
        await start_handler(message, state)
        return
    place = await search_places_by_name_obj(message.text)
    context = await make_context_text(place)
    await message.answer(context)


@router.message(Command("moderator"))
async def moderator_handler(message: types.Message, state: FSMContext):
    user = await user_detail_obj(message.from_user.id)
    if user and user.role == UserRole.MODERATOR or user.role == UserRole.ADMIN:
        role = user.get_readable_role()
        btn = await add_place()
        await message.answer(f"Xush kelibsiz, xurmatli - {role}", reply_markup=btn)


@router.callback_query(F.data == "add_place")
async def add_place_handler(call: types.CallbackQuery, state: FSMContext):
    btn = await cancel_btn()
    await call.message.delete()
    await call.message.answer("Tarixiy joyning nomini kiriting: ", reply_markup=btn)
    await state.set_state(HistoricalPlaces.title)


@router.message(F.text == "❌ Bekor qilish")
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi", reply_markup=remove_btn)
    await moderator_handler(message, state)


@router.message(HistoricalPlaces.title)
async def historical_place_title_handler(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    btn = await cancel_btn()
    await message.answer("Ushbu joy uchun izoh kiriting:", reply_markup=btn)
    await state.set_state(HistoricalPlaces.description)


@router.message(HistoricalPlaces.description)
async def historical_place_desc_handler(message: types.Message, state: FSMContext):
    desc = message.text
    await state.update_data(description=desc)
    btn = await location_btn(with_cancel=True)
    await message.answer("Lokatsiya yuboring:", reply_markup=btn)
    await state.set_state(HistoricalPlaces.location)
