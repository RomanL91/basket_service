from uuid import UUID
from enum import Enum
from decimal import Decimal
from datetime import datetime
from typing import Annotated, Optional, Type
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr,
    field_validator,
    AwareDatetime,
)

from core.base_model import TokenSchema


# Определение перечисления для типов доставки, аналогичное SQLAlchemy
class DeliveryType(str, Enum):
    DELIVERY = "DELIVERY"
    PICKUP = "PICKUP"


class PaymentType(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class PaymentStatus(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"


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


class BankCallbackModel(BaseModel):
    account_id: Annotated[str, Field(alias="accountId")]
    amount: Annotated[Decimal, Field(gt=0)]
    approval_code: Annotated[Optional[str], Field(alias="approvalCode", default=None)]
    card_id: Annotated[Optional[str], Field(alias="cardId", default=None)]
    card_mask: Annotated[str, Field(alias="cardMask")]
    card_type: Annotated[str, Field(alias="cardType")]
    code: Annotated[str, Field(alias="code")]
    currency: Annotated[str, Field(alias="currency")]
    date_time: Annotated[AwareDatetime, Field(alias="dateTime")]
    description: Annotated[Optional[str], Field(alias="description", default=None)]
    email: Annotated[Optional[str], Field(alias="email", default=None)]
    id: Annotated[UUID, Field(alias="id")]
    invoice_id: Annotated[str, Field(alias="invoiceId")]
    ip: Annotated[str, Field(alias="ip")]
    ip_city: Annotated[Optional[str], Field(alias="ipCity", default=None)]
    ip_country: Annotated[Optional[str], Field(alias="ipCountry", default=None)]
    ip_district: Annotated[Optional[str], Field(alias="ipDistrict", default=None)]
    ip_latitude: Annotated[Optional[float], Field(alias="ipLatitude", default=None)]
    ip_longitude: Annotated[Optional[float], Field(alias="ipLongitude", default=None)]
    ip_region: Annotated[Optional[str], Field(alias="ipRegion", default=None)]
    issuer: Annotated[Optional[str], Field(alias="issuer", default=None)]
    language: Annotated[Optional[str], Field(alias="language", default=None)]
    name: Annotated[Optional[str], Field(alias="name", default=None)]
    phone: Annotated[Optional[str], Field(alias="phone", default=None)]
    reason: Annotated[str, Field(alias="reason")]
    reason_code: Annotated[int, Field(alias="reasonCode")]
    reference: Annotated[str, Field(alias="reference")]
    secure: Annotated[str, Field(alias="secure")]
    secure_details: Annotated[Optional[str], Field(alias="secureDetails", default=None)]
    terminal: Annotated[str, Field(alias="terminal")]

    # Настройка модели через ConfigDict
    model_config = ConfigDict(
        populate_by_name=True,  # Разрешает доступ к полям по их "нормальному" имени
        from_attributes=True,  # Поддержка создания моделей из объектов
    )
