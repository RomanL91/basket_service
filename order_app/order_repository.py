from order_app.models import Order
from core.base_repository import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order
