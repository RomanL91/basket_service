from core.settings import settings

from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)


class DataBaseManager:
    def __init__(self, url: str, echo: bool, future: bool = False) -> None:
        self.engine = create_async_engine(url=url, echo=echo, future=future)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scope_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scope_session_dependency(self):
        session = self.get_scope_session()
        yield session
        await session.close()


db_manager = DataBaseManager(
    url=settings.db.url, echo=settings.db.echo, future=settings.db.future
)
