from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def create_obj():
        raise NotImplementedError

    @abstractmethod
    async def get_all_objs():
        raise NotImplementedError

    @abstractmethod
    async def get_obj():
        raise NotImplementedError

    @abstractmethod
    async def update_obj():
        raise NotImplementedError

    @abstractmethod
    async def delete_obj():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_obj(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all_objs(self):
        stmt = select(self.model).order_by(self.model.id)
        result: Result = await self.session.execute(stmt)
        res = result.scalars().all()
        return res

    async def get_obj(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        try:
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            return res
        except NoResultFound as e:
            raise NoResultFound(e)

    async def update_obj(self, uuid_id: str, data: dict):
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(uuid_id=uuid_id)
            .returning(self.model)
        )
        try:
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except NoResultFound as e:
            raise NoResultFound(e)

    async def delete_obj(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
