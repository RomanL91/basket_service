from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from datetime import datetime

from core import settings


# функция получения времени
def get_current_time():
    return datetime.now(settings.time_zone).replace(tzinfo=None)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=get_current_time,
        nullable=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=get_current_time,
        onupdate=get_current_time,
        nullable=True,
    )


#  =========================== Pydantic model ===========================
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator
from core.base_utils import check_token


class TokenSchema(BaseModel):
    model_config = ConfigDict(
        strict=True,  # мы строгие
        from_attributes=True,  # напрямую из атрибутов объекта, а не из словаря
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        },
    )
    access_token: Annotated[str | dict, Field(description="JWT токен для доступа")]

    @field_validator("access_token")
    def validate_jwt(jwt_value: str):
        payload = check_token(jwt_value)
        if not payload:
            raise ValueError("Не валидный ключ!")
        return payload
