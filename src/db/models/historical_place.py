from . import Base, BaseMixin, Mapped, mapped_column, Text


class HistoricalPlace(Base, BaseMixin):
    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    lat: Mapped[float]
    long: Mapped[float]
    address: Mapped[str] = mapped_column(nullable=True)

    def __str__(self):
        return self.title


