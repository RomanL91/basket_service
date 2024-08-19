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
    CANCELED = "CANCELED"


# Pydantic модель
class OrderPydantic(BaseModel):
    model_config = ConfigDict(
        strict=True,
    )

    uuid_id: Annotated[
        str,
        Field(
            ...,
            description="Уникальный идентификатор заказа, наследуется от корзины.",
            examples=["fcff9649-c7cc-498c-8ee2-c84785a68521"],
        ),
    ] = None
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
    ] = None
    comment: Annotated[
        str | None,
        Field(
            ...,
            description="Комментарий к заказу.",
            examples=[
                "Очень жду доставку. Если что, вот мой другой номер - +77782346754."
            ],
        ),
    ] = None
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
    ] = None
    delivery_address: Annotated[
        str | None,
        Field(
            ...,
            description="Адрес доставки (указывает пользователь, форма свободная).",
            examples=["Улица Достык, 8/4."],
        ),
    ] = None
    manager_executive: Annotated[
        str | None,
        Field(
            ...,
            description="Менежер, принявщий заявку.",
            examples=["Иванов Иван"],
        ),
    ] = None
    manager_executive_id: Annotated[
        str | None,
        Field(
            ...,
            description="ИД менеджера, принявщего заявку.",
            examples=[34],
        ),
    ] = None
    manager_mailbox: Annotated[
        str | None,
        Field(
            ...,
            description="Почтовый ящик менеджера.",
            examples=["Ivanov@example.com"],
        ),
    ] = None
    # created_at: Annotated[
    #     datetime | None,
    #     Field(
    #         ...,
    #         description="Время создания ордера в системе.",
    #         examples=["2024-08-07T23:54:51.628882"],
    #     ),
    # ] = None
    # updated_at: Annotated[
    #     datetime | None,
    #     Field(
    #         ...,
    #         description="Время обновления ордера в системе.",
    #         examples=["2024-08-07T23:54:51.628882"],
    #     ),
    # ] = None


class CreateOrderPydantic(OrderPydantic):
    model_config = ConfigDict(
        strict=True,
        json_schema_extra={
            "example": {
                "uuid_id": "fcff9649-c7cc-498c-8ee2-c84785a68521",
                "phone_number": "+77714658976",
                "shipping_city": "Астана",
                "delivery_address": "Улица Достык, 8/4.",
            }
        },
    )

    uuid_id: str
    phone_number: str
    shipping_city: str
    delivery_address: str


class ReadOrderPydantic(OrderPydantic):
    created_at: datetime | None
    updated_at: datetime | None


class UpdateOrderPydantic(OrderPydantic):
    pass
