from abc import ABC, abstractmethod

from basket_app.bascket_repository import BascketRepository
from core.db_manager import db_manager
from order_app.order_repository import OrderRepository, TransactionPaymentRepository


class IUnitOfWork(ABC):

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = db_manager.get_scope_session()

    async def __aenter__(self):
        self.session = self.session_factory()
        # для работы
        self.bascket = BascketRepository(self.session)
        self.order = OrderRepository(self.session)
        self.payment = TransactionPaymentRepository(self.session)

    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
