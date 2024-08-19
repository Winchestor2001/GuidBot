import logging

from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from markupsafe import Markup
from src.settings import settings

logger = logging.getLogger("fastapi_app")


# class ProductImageAdmin(ModelView, model=ProductImage):
#     column_list = [ProductImage.uuid, ProductImage.image, ProductImage.product]
#     column_searchable_list = [ProductImage.uuid]
#
#     column_formatters = {
#         'image': lambda model, field: Markup(
#             f'<a href="{model.image}" target="_blank">'
#             f'<img src="{model.image}" style="height:50px;" />'
#             f'</a>'
#         )
#     }
#     column_formatters_detail = {
#         'image': lambda model, field: Markup(
#             f'<a href="{model.image}" target="_blank">'
#             f'<img src="{model.image}" style="height:150px;" />'
#             f'</a>'
#         )
#     }


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
