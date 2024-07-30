from sqlalchemy import UniqueConstraint
from sqlalchemy.types import JSON 
# from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base

class Basket(Base):
    __table_args__ = (
        UniqueConstraint("uuid_id"),
        UniqueConstraint("created_at"),
    )
    # уникальный код от клиентской стороны
    uuid_id: Mapped[str] = mapped_column()
    # id пользователя, если набирал корзину аутентифицированным (достать с JWT)
    user_id: Mapped[int] = mapped_column(
        nullable=True,
    )
    # стаус корзины, сменяется на TRUE если на корзину заключен ордер
    completed: Mapped[bool] = mapped_column(
        default=False,
        nullable=True,
    )
    # список словарей {"count": 3, "prod_id": 2} - состав корзины
    basket_items: Mapped[list] = mapped_column(
        JSON,
        default=list,
    )
    # orders = relationship("Order", back_populates="basket")

    def __str__(self):
        return f"Basket id={self.id}, uuid_id={self.uuid_id!r})"

    def __repr__(self):
        return str(self)



# ========================================================================
# модель ордера
# from enum import Enum

# # Определение перечисления для типов доставки
# class DeliveryType(Enum):
#     PICKUP = "Самовывоз"
#     DELIVERY = "Доставка продавца"


# class Order(Base):
#     uuid_id: Mapped[str] = mapped_column(
#         ForeignKey("baskets.uuid_id"),
#         unique=True,
#     )
#     order_status: Mapped[str] = mapped_column()
#     comment: Mapped[str] = mapped_column(
#         Text,
#         nullable=True,
#     )
#     phone_number: Mapped[str] = mapped_column()  # Номер телефона для контакта
#     shipping_city: Mapped[str] = mapped_column()  # Город отгрузки
#     delivery_address: Mapped[str] = mapped_column()  # Адрес доставки
#     delivery_type: Mapped[DeliveryType] = mapped_column(
#         SQLEnum(DeliveryType),
#     )  # Тип доставки, например "Самовывоз" или "Доставка продавца"
#     # Связь с моделью корзины
#     basket: Mapped["Basket"] = relationship(
#         "Basket",
#         back_populates="orders",
#     )
#     completed: Mapped[bool] = mapped_column(
#         default=False,
#         nullable=True,
#     )

#     def __str__(self):
#         return f"Order id={self.id}, uuid_id={self.uuid_id!r})"

#     def __repr__(self):
#         return str(self)
