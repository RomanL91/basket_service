from decimal import Decimal
from random import randint

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Text, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from sqlalchemy.dialects.postgresql import JSON

from core import Base
from order_app.schemas import DeliveryType, OrderStatusType, PaymentType


class Order(Base):
    # ФИО пользователя, который создал заказ
    user_full_name: Mapped[str] = mapped_column(
        nullable=False,
    )
    # Общая сумма заказа, с точностью до двух десятичных знаков
    total_amount: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), 
        nullable=False, 
        default=0.0,
    )
    # Номер счета для банка, автоматически генерируется
    account_number: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        unique=True,
        default=lambda: randint(100000000, 999999999),
    )
    # Тип оплаты
    payment_type: Mapped[PaymentType] = mapped_column(
        SQLEnum(PaymentType),
        nullable=False,
        default=PaymentType.ONLINE
    )
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
        nullable=False,
        default=DeliveryType.DELIVERY
    )
    # Связь с моделью корзины
    basket: Mapped["Basket"] = relationship(  # type: ignore
        "Basket",
        back_populates="orders",
    )
    manager_executive: Mapped[str] = mapped_column(
        nullable=True,
    )
    manager_executive_id: Mapped[str] = mapped_column(
        nullable=True,
    )
    manager_mailbox: Mapped[str] = mapped_column(
        nullable=True,
    )

    def __str__(self):
        return f"Order id={self.id}, uuid_id={self.uuid_id!r})"

    def __repr__(self):
        return str(self)
