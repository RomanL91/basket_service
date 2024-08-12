from enum import Enum
from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# Определение перечисления для типов доставки, аналогичное SQLAlchemy
class DeliveryType(str, Enum):
    DELIVERY = "DELIVERY"
    PICKUP = "PICKUP"


class OrderStatusType(str, Enum):
    NEW = "NEW"
    INWORK = "INWORK"
    COMPLITED = "COMPLITED"


# Pydantic модель
class OrderPydantic(BaseModel):
    model_config = ConfigDict(strict=True)

    uuid_id: Annotated[
        str,
        Field(
            ...,
            description="Уникальный идентификатор заказа, наследуется от корзины.",
            examples=["fcff9649-c7cc-498c-8ee2-c84785a68521"],
        ),
    ]
    order_status: Annotated[
        OrderStatusType | str,
        Field(
            ...,
            description="Текущий статус заказа. Значение по умолчанию NEW.",
            examples=[OrderStatusType.NEW],
        ),
    ] = OrderStatusType.NEW
    phone_number: Annotated[
        str,
        Field(
            ...,
            description="Номер телефона для контакта.",
            examples=["+77714658976"],
        ),
    ]
    comment: Annotated[
        str | None,
        Field(
            ...,
            description="Комментарий к заказу.",
            examples=[
                "Очень жду доставку. Если что, вот мой другой номер - +77782346754."
            ],
        ),
    ]
    delivery_type: Annotated[
        DeliveryType | str,
        Field(
            ...,
            description="Тип доставки (выбирает пользователь, по умолчанию - силами продовца).",
            examples=[DeliveryType.DELIVERY],
        ),
    ] = DeliveryType.DELIVERY
    shipping_city: Annotated[
        str,
        Field(
            ...,
            description="Город отгрузки (важно: выбор делает софт, не пользователь).",
            examples=["Астана"],
        ),
    ]
    delivery_address: Annotated[
        str | None,
        Field(
            ...,
            description="Адрес доставки (указывает пользователь, форма свободная).",
            examples=["Улица Достык, 8/4."],
        ),
    ]
    created_at: Annotated[
        datetime | None,
        Field(
            ...,
            description="Время создания ордера в системе.",
            examples=["2024-08-07T23:54:51.628882"],
        ),
    ]
    updated_at: Annotated[
        datetime | None,
        Field(
            ...,
            description="Время обновления ордера в системе.",
            examples=["2024-08-07T23:54:51.628882"],
        ),
    ]
