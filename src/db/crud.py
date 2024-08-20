from sqlalchemy import select

from src.db import db_helper, User, HistoricalPlace
from src.db.utils import haversine


async def create_user_obj(telegram_id: int, username: str):
    async with db_helper.session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user_obj = result.scalars().first()

        if not user_obj:
            user_obj = User(telegram_id=telegram_id, username=username)
            session.add(user_obj)
            await session.commit()

        return user_obj


async def user_detail_obj(telegram_id: int):
    async with db_helper.session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user_obj = result.scalars().first()
        return user_obj


async def create_history_place_obj(title: str, description: str, latitude: float, longitude: float, address: str):
    async with db_helper.session_factory() as session:
        place_obj = HistoricalPlace(title=title, description=description, lat=latitude, long=longitude, address=address)
        session.add(place_obj)
        await session.commit()

        return place_obj


async def search_places_obj(lat: float, long: float, radius_m: int = 500):
    async with db_helper.session_factory() as session:
        result = await session.execute(select(HistoricalPlace))
        places = result.scalars().all()

        nearby_places = [
            place for place in places
            if haversine(lat, long, place.lat, place.long) <= radius_m
        ]

        return nearby_places


async def search_places_by_name_obj(title: str):
    async with db_helper.session_factory() as session:
        result = await session.execute(select(HistoricalPlace).where(HistoricalPlace.title == title))
        places = result.scalars().first()
        return places
