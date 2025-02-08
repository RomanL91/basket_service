from datetime import datetime, timezone, timedelta

from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound

from order_app.models import Order, TransactionPayment
from core.base_repository import SQLAlchemyRepository


class TransactionPaymentRepository(SQLAlchemyRepository):
    model = TransactionPayment

    async def create_obj_pay(self, **data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()


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

    async def get_objs_to_user_id(self, user_id: str):
        stmt = (
            select(self.model)
            .filter_by(user_id=user_id)
            .order_by(self.model.created_at)
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_obj(
        self,
        max_age_days: int | None = None,
        **filter_by,
    ):
        stmt = select(self.model).filter_by(**filter_by)

        if max_age_days is not None and hasattr(self.model, "created_at"):
            min_date = datetime.now(timezone.utc) - timedelta(days=max_age_days)
            stmt = stmt.where(self.model.created_at >= min_date)
        try:
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            return res
        except NoResultFound:
            return None
