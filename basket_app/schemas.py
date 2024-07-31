import re

from datetime import datetime
from typing import Annotated, List, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator


class SimpleMSGErrorPydantic(BaseModel):
    status_code: int
    message: str


class BasketPydantic(BaseModel):
    model_config = ConfigDict(strict=True)

    uuid_id: Annotated[
        str,
        Field(
            ...,
            description="Уникальный ID с клиента",
            examples=["fcff9649-c7cc-498c-8ee2-c84785a68521"],
        ),
    ] = None
    user_id: Annotated[
        int | str | None,
        Field(
            ...,
            description="Уникальный ID пользователя",
            examples=[789],
        ),
    ] = None
    completed: Annotated[
        bool | None,
        Field(
            ...,
            description="Статус корзины",
            examples=[False],
        ),
    ] = False
    basket_items: Annotated[
        List[Dict[str, int]] | None,
        Field(
            ...,
            description="Состав корзины",
            example=[
                {
                    "prod_id": 1,
                    "count": 5,
                    "price": 799,
                },
                {
                    "prod_id": 2,
                    "count": 3,
                    "price": 4599,
                },
            ],
        ),
    ] = None


# ========================================================================
# модель ордера
# from enum import Enum


# class DeliveryType(str, Enum):
#     PICKUP = "Самовывоз"
#     DELIVERY = "Доставка продавца"

# class OrderPydantic(BaseModel):
#     model_config = ConfigDict(strict=True)

#     uuid_id: str
#     order_status: str
#     comment: str | None = None
#     phone_number: str
#     shipping_city: str
#     delivery_address: str
#     delivery_type: DeliveryType
#     completed: bool | None = False
#     created_at: datetime | None = None
#     updated_at: datetime | None = None

#     # class Config:
#     #     orm_mode = True

#     @field_validator("phone_number")
#     def validate_phone_number(cls, v):
#         if not re.match(r"^\+?[1-9]\d{1,14}$", v):
#             raise ValueError("Invalid phone number format")
#         return v

#     @field_validator("delivery_type")
#     def validate_delivery_type(cls, v):
#         if v not in [choice.value for choice in DeliveryType]:
#             raise ValueError("Invalid delivery type")
#         return v
