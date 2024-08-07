from sqlalchemy import select
from sqlalchemy.orm import joinedload

from order_app.models import Order
from core.base_repository import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def get_info_order_with_basket(self, uuid_id: str):
        stmt = (
            select(Order)
            .options(joinedload(Order.basket))  # Загрузка связанных данных корзины
            .filter(Order.uuid_id == uuid_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()
