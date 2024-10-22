from basket_app.models import Basket
from core.base_repository import SQLAlchemyRepository
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select


class BascketRepository(SQLAlchemyRepository):
    model = Basket

    async def get_obj(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        try:
            res = await self.session.execute(stmt)
            obj = res.scalars().first()
            if res is None:
                raise NoResultFound
            return obj
        except NoResultFound as e:
            raise NoResultFound(e)

    async def create_or_update(self, uuid_id: str, data: dict):
        try:
            # Пытаемся найти объект по UUID
            existing_obj = await self.get_obj(uuid_id=uuid_id)
            # Если объект найден, обновляем его
            return await self.update_obj(uuid_id, data)
        except NoResultFound as error:
            return await self.create_obj(data)
