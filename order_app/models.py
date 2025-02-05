from decimal import Decimal
from random import randint
from datetime import datetime

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Text, DECIMAL, Integer, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from sqlalchemy.dialects.postgresql import JSON

from core import Base
from order_app.schemas import DeliveryType, OrderStatusType, PaymentType, PaymentStatus


class Order(Base):
    # ФИО пользователя, который создал заказ
    user_full_name: Mapped[str] = mapped_column(
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
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
        SQLEnum(PaymentType), nullable=False, default=PaymentType.ONLINE
    )
    # унаследуем от корзины
    uuid_id: Mapped[str] = mapped_column(
        ForeignKey("baskets.uuid_id"),
        unique=False,
    )
    # статус заявки [новая, в работе, выполнена]
    order_status: Mapped[OrderStatusType] = mapped_column(
        SQLEnum(OrderStatusType), default=OrderStatusType.NEW
    )
    # статус платежа ордера [оплачено, неоплачено]
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus), default=PaymentStatus.UNPAID
    )
    # комментарий к заявке от пользователя
    comment: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    # Номер телефона для контакта
    phone_number: Mapped[str] = mapped_column()
    # Email пользователя (необязательное поле)
    email: Mapped[str] = mapped_column(nullable=True)
    # Город отгрузки
    shipping_city: Mapped[str] = mapped_column()
    # Адрес доставки
    delivery_address: Mapped[str] = mapped_column(
        nullable=True,
    )
    # Тип доставки, например "Самовывоз" или "Доставка продавца"
    delivery_type: Mapped[DeliveryType] = mapped_column(
        SQLEnum(DeliveryType), nullable=False, default=DeliveryType.DELIVERY
    )
    # Связь с моделью корзины
    basket: Mapped["Basket"] = relationship(  # type: ignore
        "Basket",
        back_populates="orders",
    )
    # Связь с платежами
    transactions: Mapped["TransactionPayment"] = relationship(
        "TransactionPayment", back_populates="order", cascade="all, delete-orphan"
    )
    # Поле для хранения ссылки на платежку банка
    payment_link: Mapped[str] = mapped_column(
        nullable=True,
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


# куда ж ты городишь это...
class TransactionPayment(Base):
    account_id: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    approval_code: Mapped[str] = mapped_column(nullable=False)
    card_id: Mapped[str | None] = mapped_column(nullable=True)
    card_mask: Mapped[str | None] = mapped_column(nullable=True)
    card_type: Mapped[str | None] = mapped_column(nullable=True)
    code: Mapped[str] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(nullable=False)
    date_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str | None] = mapped_column(nullable=True)
    ip: Mapped[str] = mapped_column(nullable=True)
    ip_city: Mapped[str | None] = mapped_column(nullable=True)
    ip_country: Mapped[str | None] = mapped_column(nullable=True)
    ip_district: Mapped[str | None] = mapped_column(nullable=True)
    ip_latitude: Mapped[float | None] = mapped_column(nullable=True)
    ip_longitude: Mapped[float | None] = mapped_column(nullable=True)
    ip_region: Mapped[str | None] = mapped_column(nullable=True)
    issuer: Mapped[str | None] = mapped_column(nullable=True)
    language: Mapped[str | None] = mapped_column(nullable=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    phone: Mapped[str | None] = mapped_column(nullable=True)
    reason: Mapped[str] = mapped_column(nullable=False)
    reason_code: Mapped[int] = mapped_column(Integer, nullable=False)
    reference: Mapped[str] = mapped_column(unique=True, nullable=False)
    secure: Mapped[str | None] = mapped_column(nullable=True)
    secure_details: Mapped[str | None] = mapped_column(nullable=True)
    terminal: Mapped[str] = mapped_column(nullable=False)
    invoice_id: Mapped[str] = mapped_column(
        ForeignKey("orders.account_number"), nullable=False
    )
    order: Mapped["Order"] = relationship("Order", back_populates="transactions")

    def __str__(self):
        return f"Transaction {self.account_id!r}, amount {self.amount!r}"

    def __repr__(self):
        return str(self)
