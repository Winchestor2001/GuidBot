from aiogram.fsm.state import StatesGroup, State


class Places(StatesGroup):
    place = State()


class HistoricalPlaces(StatesGroup):
    title = State()
    description = State()
    location = State()
