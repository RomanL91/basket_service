from sqlalchemy import select
from sqlalchemy.orm import joinedload

from order_app.models import Order
from core.base_repository import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order

    def get_query_orders(self, order_status):
        return (
            select(self.model)
            .where(self.model.order_status == order_status)
            .order_by(self.model.created_at)
        )

    async def get_info_order_with_basket(self, uuid_id: str):
        stmt = (
            select(Order)
            .options(joinedload(Order.basket))  # Загрузка связанных данных корзины
            .filter(Order.uuid_id == uuid_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    def get_objs_by_filters(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by).order_by(self.model.created_at)
        return stmt
