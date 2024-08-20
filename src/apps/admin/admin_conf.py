import logging

from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.db import User, HistoricalPlace
from src.settings import settings

logger = logging.getLogger("fastapi_app")


class UserAdmin(ModelView, model=User):
    column_list = [User.telegram_id, User.username, User.role]
    column_searchable_list = [User.telegram_id, User.username]


class HistoricalPlaceAdmin(ModelView, model=HistoricalPlace):
    column_list = [HistoricalPlace.title, HistoricalPlace.lat, HistoricalPlace.long]
    column_searchable_list = [HistoricalPlace.title]


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username in settings.admin.usernames and password in settings.admin.passwords:
            # Validate username/password credentials
            # And update session
            request.session.update({"token": "..."})

            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True
