from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# Определение перечисления для типов доставки, аналогичное SQLAlchemy
class DeliveryType(str, Enum):
    DELIVERY = "DELIVERY"
    PICKUP = "PICKUP"


# Pydantic модель
class OrderPydantic(BaseModel):
    uuid_id: str = Field(
        ..., description="Уникальный идентификатор заказа, связанный с корзиной"
    )
    order_status: str = Field(..., description="Текущий статус заказа")
    comment: Optional[str] = Field(None, description="Комментарий к заказу")
    phone_number: str = Field(..., description="Номер телефона для контакта")
    shipping_city: str = Field(..., description="Город отгрузки")
    delivery_address: Optional[str] = Field(None, description="Адрес доставки")
    delivery_type: Optional[DeliveryType] = Field(None, description="Тип доставки")
    completed: bool = Field(False, description="Статус завершённости заказа")
    basket_uuid: str = Field(
        ..., description="Уникальный идентификатор корзины, связанной с заказом"
    )
