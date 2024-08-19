from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, Float, Enum
from typing import List, TYPE_CHECKING
from src.db.base import Base, BaseMixin
import enum


class UserRole(enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
