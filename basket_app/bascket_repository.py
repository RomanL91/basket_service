from basket_app.models import Basket
from core.base_repository import SQLAlchemyRepository


class BascketRepository(SQLAlchemyRepository):
    model = Basket

    async def create_or_update(self, uuid_id: str, data: dict):
        # Пытаемся найти объект по UUID
        existing_obj = await self.get_obj(uuid_id=uuid_id)

        if existing_obj is None:
            # Если объект не найден, создаем новый
            return await self.create_obj(data)
        else:
            # Если объект найден, обновляем его
            return await self.update_obj(uuid_id, data)
