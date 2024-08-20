from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove


remove_btn = ReplyKeyboardRemove()


async def location_btn(with_cancel: bool = False):
    keyboard = ReplyKeyboardBuilder()
    if with_cancel:
        keyboard.row(
            KeyboardButton(text="❌ Bekor qilish")
        )
    keyboard.row(
        KeyboardButton(text="📍 Lokatsiya", request_location=True)
    )
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


async def places_btn(objs):
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text="🔙 Ortga")
    )
    for item in objs:
        keyboard.add(
            KeyboardButton(text=f"{item.title[:20]}")
        )
    keyboard.adjust(1, 2)
    return keyboard.as_markup(resize_keyboard=True)


async def cancel_btn():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text="❌ Bekor qilish")
    )
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


async def add_place():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="➕ Joy qo'shish", callback_data="add_place"),
    )
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)
