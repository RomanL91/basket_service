from sqlalchemy import Enum as SQLEnum
from sqlalchemy import UniqueConstraint
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from sqlalchemy.dialects.postgresql import JSON

from core import Base

from basket_app.schemas import CheckoutStageSchema


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
