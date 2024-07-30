from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from datetime import datetime

from core import settings


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(settings.time_zone),
        nullable=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(settings.time_zone),
        onupdate=lambda: datetime.now(settings.time_zone),
        nullable=True,
    )
