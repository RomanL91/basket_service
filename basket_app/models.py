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
    orders = relationship("Order", back_populates="basket")

    def __str__(self):
        return f"Basket id={self.id}, uuid_id={self.uuid_id!r})"

    def __repr__(self):
        return str(self)
