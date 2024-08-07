import jwt
import httpx

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# == My
from core import settings
from core.base_UOW import IUnitOfWork
from basket_app.models import Basket
from basket_app.schemas import BasketPydantic

from typing import List


class BascketService:
    async def create_bascket(
        self, uow: IUnitOfWork, new_bascket: BasketPydantic
    ) -> Basket | None:
        # получаем продукты по апи из сервиса магазина
        prod_ids = [item["prod_id"] for item in new_bascket.basket_items]
        product_details = await self.fetch_product_details(prod_ids, new_bascket)
        new_bascket = product_details

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
        # достаем ИД пользователя из JWT
        user_id = self.extract_user_id_from_jwt(bascket_data.user_id)
        bascket_data.user_id = user_id
        # получаем продукты по апи из сервиса магазина
        prod_ids = (
            [item["prod_id"] for item in bascket_data.basket_items]
            if bascket_data.basket_items is not None
            else []
        )
        product_details = await self.fetch_product_details(prod_ids, bascket_data)
        bascket_data = product_details

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

    # TODO можно вынести в файл/класс утилит ==============================
    # функция утилита для извлечения ИД из токена
    def extract_user_id_from_jwt(self, jwt_token: str | None) -> int | None:
        if jwt_token is not None:
            try:
                decoded = jwt.decode(
                    jwt_token, settings.auth_jwt.public_key, settings.auth_jwt.algorithm
                )
                return decoded["user_id"]
            except jwt.PyJWTError as e:
                raise HTTPException(status_code=400, detail=f"Недействительный JWT.")
        return jwt_token

    async def fetch_product_details(
        self, prod_ids: List[int], new_bascket: BasketPydantic
    ) -> BasketPydantic:
        prod_ids_str = ",".join(map(str, prod_ids))
        url = settings.api_shop.get_prod_by_ids(prod_ids_str=prod_ids_str)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()  # Проверка на HTTP ошибки
                details_dict = {detail["id"]: detail for detail in response.json()}
                list_prod_gifts_ids = []
                for item in new_bascket.basket_items:
                    prod_detail = details_dict.get(item["prod_id"])
                    if prod_detail:
                        item["prod"] = prod_detail
                        item["name"] = prod_detail["name_product"]
                        item["slug"] = prod_detail["slug"]
                        item["url"] = settings.api_shop.get_url_admin_prod_detail(
                            prod_id=prod_detail["id"]
                        )
                        item["urlapi"] = settings.api_shop.get_url_api_prod_detail(
                            prod_slug=item["slug"]
                        )
                    if "gift_prod_id" in item:
                        list_prod_gifts_ids.append(item["gift_prod_id"])
                prod_gift_ids_str = ",".join(map(str, list_prod_gifts_ids))
                url_gift_prod = settings.api_shop.get_prod_by_ids(
                    prod_ids_str=prod_gift_ids_str
                )
                response_gift_prod = await client.get(url_gift_prod)
                if response_gift_prod.status_code != 200:
                    return new_bascket
                new_bascket.gift_items = response_gift_prod.json()
                return new_bascket
        except httpx.HTTPStatusError as e:
            raise AttributeError("Корзине нужны продукты")

        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
