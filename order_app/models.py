from enum import Enum

from sqlalchemy import Enum as SQLEnum

from sqlalchemy import ForeignKey, Text

# from sqlalchemy.dialects.postgresql import JSON

from basket_app.models import Basket
from core import Base


from sqlalchemy.orm import Mapped, mapped_column, relationship


# Определение перечисления для типов доставки
class DeliveryType(Enum):
    PICKUP = "PICKUP"
    DELIVERY = "DELIVERY"


class Order(Base):
    uuid_id: Mapped[str] = mapped_column(
        ForeignKey("baskets.uuid_id"),
        unique=True,
    )
    order_status: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    phone_number: Mapped[str] = mapped_column()  # Номер телефона для контакта
    shipping_city: Mapped[str] = mapped_column()  # Город отгрузки
    delivery_address: Mapped[str] = mapped_column(
        nullable=True,
    )  # Адрес доставки
    delivery_type: Mapped[DeliveryType] = mapped_column(
        SQLEnum(DeliveryType),
        nullable=True,
    )  # Тип доставки, например "Самовывоз" или "Доставка продавца"
    # Связь с моделью корзины
    basket: Mapped["Basket"] = relationship(
        "Basket",
        back_populates="orders",
    )
    completed: Mapped[bool] = mapped_column(
        default=False,
        nullable=True,
    )

    def __str__(self):
        return f"Order id={self.id}, uuid_id={self.uuid_id!r})"

    def __repr__(self):
        return str(self)
