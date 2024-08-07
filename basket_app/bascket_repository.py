from basket_app.models import Basket
from core.base_repository import SQLAlchemyRepository
from sqlalchemy.exc import NoResultFound


class BascketRepository(SQLAlchemyRepository):
    model = Basket

    async def create_or_update(self, uuid_id: str, data: dict):
        try:
            # Пытаемся найти объект по UUID
            existing_obj = await self.get_obj(uuid_id=uuid_id)
            # Если объект найден, обновляем его
            return await self.update_obj(uuid_id, data)
        except NoResultFound as error:
            return await self.create_obj(data)
