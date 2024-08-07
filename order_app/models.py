from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from sqlalchemy.dialects.postgresql import JSON

from core import Base
from order_app.schemas import DeliveryType, OrderStatusType


class Order(Base):
    # унаследуем от корзины
    uuid_id: Mapped[str] = mapped_column(
        ForeignKey("baskets.uuid_id"),
        unique=True,
    )
    # статус заявки [новая, в работе, выполнена]
    order_status: Mapped[OrderStatusType] = mapped_column(
        SQLEnum(OrderStatusType), default=OrderStatusType.NEW
    )
    # комментарий к заявке от пользователя
    comment: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    # Номер телефона для контакта
    phone_number: Mapped[str] = mapped_column()
    # Город отгрузки
    shipping_city: Mapped[str] = mapped_column()
    # Адрес доставки
    delivery_address: Mapped[str] = mapped_column(
        nullable=True,
    )
    # Тип доставки, например "Самовывоз" или "Доставка продавца"
    delivery_type: Mapped[DeliveryType] = mapped_column(
        SQLEnum(DeliveryType),
        nullable=True,
    )
    # Связь с моделью корзины
    basket: Mapped["Basket"] = relationship(  # type: ignore
        "Basket",
        back_populates="orders",
    )

    def __str__(self):
        return f"Order id={self.id}, uuid_id={self.uuid_id!r})"

    def __repr__(self):
        return str(self)
