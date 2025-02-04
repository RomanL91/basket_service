from sqlalchemy import Enum as SQLEnum
from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey, Text, DECIMAL, Integer, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from basket_app.schemas import CheckoutStageSchema
from core import Base

# from sqlalchemy.dialects.postgresql import JSON


class Basket(Base):
    __table_args__ = (
        UniqueConstraint("uuid_id"),
        UniqueConstraint("created_at"),
    )
    # уникальный код от клиентской стороны
    uuid_id: Mapped[str] = mapped_column()
    # id пользователя, если набирал корзину аутентифицированным (достать с JWT)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    # стаус корзины, сменяется на TRUE если на корзину заключен ордер
    completed: Mapped[bool] = mapped_column(
        default=False,
        nullable=True,
    )
    # Этап оформления
    checkout_stage: Mapped[CheckoutStageSchema] = mapped_column(
        SQLEnum(CheckoutStageSchema),
        nullable=False,
        default=CheckoutStageSchema.CREATED,
    )
    # список словарей {"count": 3, "prod_id": 2} - состав корзины
    basket_items: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    gift_items: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    orders: Mapped["Order"] = relationship(  # type: ignore
        "Order",
        back_populates="basket",
    )

    def __str__(self):
        return f"Basket id={self.id}, uuid_id={self.uuid_id!r})"

    def __repr__(self):
        return str(self)
