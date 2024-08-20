from . import Base, BaseMixin, Mapped, mapped_column, BigInteger, UserRole, Enum


class User(Base, BaseMixin):
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True, unique=True)
    username: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.username
