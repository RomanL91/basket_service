import jwt

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# == My
from core import settings
from core.base_UOW import IUnitOfWork
from basket_app.models import Basket
from basket_app.schemas import BasketPydantic


class BascketService:
    async def create_bascket(
        self, uow: IUnitOfWork, new_bascket: BasketPydantic
    ) -> Basket | None:
        bascket_dict = new_bascket.model_dump()
        async with uow:
            try:
                bascket = await uow.bascket.create_obj(bascket_dict)
                await uow.commit()
                return bascket
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Корзина {new_bascket.uuid_id!r} уже существует.",
                )

    async def get_baskets(self, uow: IUnitOfWork) -> list[Basket]:
        async with uow:
            return await uow.bascket.get_all_objs()

    async def get_bascket_by_uuid(self, uow: IUnitOfWork, uuid_id: str) -> Basket:
        async with uow:
            return await uow.bascket.get_obj(uuid_id=uuid_id, completed=False)

    async def update_bascket(
        self,
        uow: IUnitOfWork,
        uuid_id: str,
        bascket_update: BasketPydantic,
        partial: bool = False,
    ) -> Basket:
        data = bascket_update.model_dump(exclude_unset=partial)
        async with uow:
            bascket = await uow.bascket.update_obj(uuid_id=uuid_id, data=data)
            await uow.commit()
            return bascket

    async def delete_bascket(self, uow: IUnitOfWork, uuid_id: str) -> None:
        async with uow:
            await uow.bascket.delete_obj(uuid_id=uuid_id)
            await uow.commit()

    async def create_or_update_bascket(
        self, uow: IUnitOfWork, uuid_id: str, bascket_data: BasketPydantic
    ) -> Basket:
        user_id = self.extract_user_id_from_jwt(bascket_data.user_id)
        bascket_data.user_id = user_id
        bascket_dict = bascket_data.model_dump()
        async with uow:
            try:
                bascket = await uow.bascket.create_or_update(
                    uuid_id=uuid_id, data=bascket_dict
                )
                await uow.commit()
                return bascket
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ошибка при создании или обновлении корзины {uuid_id!r}.",
                )

    # функция утилита для извлечения ИД из токена
    # TODO можно вынести в файл/класс утилит
    def extract_user_id_from_jwt(self, jwt_token: str | None) -> int:
        if jwt_token is not None:
            try:
                decoded = jwt.decode(
                    jwt_token, settings.auth_jwt.public_key, settings.auth_jwt.algorithm
                )
                return decoded["user_id"]
            except jwt.PyJWTError as e:
                raise HTTPException(status_code=400, detail=f"Недействительный JWT.")
        return jwt_token
