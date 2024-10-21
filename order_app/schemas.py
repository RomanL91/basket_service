from enum import Enum
from datetime import datetime
from typing import Annotated, Optional, Type
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator, HttpUrl

from core.base_model import TokenSchema


# Определение перечисления для типов доставки, аналогичное SQLAlchemy
class DeliveryType(str, Enum):
    DELIVERY = "DELIVERY"
    PICKUP = "PICKUP"


class PaymentType(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class OrderStatusType(str, Enum):
    NEW = "NEW"
    INWORK = "INWORK"
    COMPLITED = "COMPLITED"
    CANCELED = "CANCELED"


class OrderCreateSchema(BaseModel):
    # Настройки модели
    model_config = ConfigDict(
        strict=True,  # мы строгие
        # use_enum_values=True, # это до сих пор не работает
        from_attributes=True,  # напрямую из атрибутов объекта, а не из словаря
        json_schema_extra={
            "example": {
                "user_full_name": "Иван Иванов",
                "payment_type": PaymentType.ONLINE,
                "uuid_id": "123e4567-e89b-12d3-a456-426614174000",
                "phone_number": "+77001234567",
                "shipping_city": "Астана",
                "delivery_address": "ул. Ленина, д. 1",
                "delivery_type": DeliveryType.DELIVERY,
                "access_token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                },
                "comment": "Позвоните перед доставкой",
                "email": "ivan@example.com",
            }
        },
    )

    @staticmethod
    def validate_enum(value: str, enum_class: Type[Enum], field_name: str):
        values = set(item.value for item in enum_class)
        if value.islower() or value not in values:
            raise ValueError(
                f"Поле '{field_name}' принимает только значения: {', '.join(values)}"
            )
        return value

    # Валидатор для payment_type и delivery_type
    @field_validator("payment_type", "delivery_type")
    def check_enum_fields(cls, v, info):
        if info.field_name == "payment_type":
            return cls.validate_enum(v, PaymentType, "payment_type")
        if info.field_name == "delivery_type":
            return cls.validate_enum(v, DeliveryType, "delivery_type")
        return v

    # Обязательные поля
    user_full_name: Annotated[
        str, Field(description="ФИО пользователя, который создал заказ")
    ]
    payment_type: Annotated[str, Field(description="Тип оплаты")]
    uuid_id: Annotated[str, Field(description="UUID корзины, связанный с заказом")]
    phone_number: Annotated[str, Field(description="Номер телефона для контакта")]
    shipping_city: Annotated[str, Field(description="Город доставки")]
    delivery_address: Annotated[str, Field(description="Адрес доставки")]
    delivery_type: Annotated[str, Field(description="Тип доставки")]
    access_token: TokenSchema
    email: Annotated[EmailStr, Field(description="Email пользователя")]
    # Необязательные поля
    comment: Annotated[
        Optional[str], Field(None, description="Комментарий к заказу")
    ] = None


# Pydantic модел
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
