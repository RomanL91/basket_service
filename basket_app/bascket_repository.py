from basket_app.models import Basket
from core.base_repository import SQLAlchemyRepository


class BascketRepository(SQLAlchemyRepository):
    model = Basket
