from fastapi import APIRouter, Header, HTTPException, status
from sqlalchemy.exc import NoResultFound

from api_v1.basket_api.depends import Token_Depends, UOF_Depends

# == My
from basket_app import schemas
from basket_app.bascket_service import BascketService
from core.base_model import TokenSchema

router = APIRouter(tags=["Bascket"])


# GET ALL       === === === === === === === ===
@router.get(
    "/",
    response_model=list[schemas.BasketPydantic],
    summary="Получение списка корзин.",
    description="Можно получить список всех корзин. А нафиг? Пока пусть будет.",
    # deprecated=True,
)
async def get_basckets(uow: UOF_Depends):
    return await BascketService().get_baskets(uow)


# GET           === === === === === === === ===
@router.get(
    "/by/{uuid_id}/",
    response_model=schemas.BasketPydantic | schemas.SimpleMSGErrorPydantic,
    summary="Получение экземпляра корзины по uuid_id.",
    description="""Нужен uuid_id для получения экземпляра корзины. 
                Вернет корзину с completed = False""",
)
async def get_bascket_by_uuid(
    uuid_id: str,
    uow: UOF_Depends,
):
    try:
        return await BascketService().get_bascket_by_uuid(uow=uow, uuid_id=uuid_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Корзина с UUID {uuid_id!r} не найдена.",
        )


@router.get(
    "/by_access_t/",
    # response_model=,
    summary="Получение экземпляра корзины через haeders access_token.",
    description="""
        Нужен валидный ключ. 
        Вернет корзину с completed = False.
        """,
)
async def get_basket_by_access_token(uow: UOF_Depends, access_token: Token_Depends):
    try:
        data_token = TokenSchema(access_token=access_token)
        user_id = data_token.access_token.get("user_id")
        basket = await BascketService().get_bascket_by_user_id(uow=uow, user_id=user_id)
        return basket
    except ValueError:
        raise HTTPException(400)


# UPDATE PATCH  === === === === === === === ===
@router.patch(
    "/{uuid_id}/",
    response_model=schemas.BasketPydantic,
    summary="Обновит поле корзины.",
    description="В теле запроса можно указать то поле, которое нужно обновить.",
)
async def update_bascket(
    uow: UOF_Depends,
    uuid_id: str,
    bascket_update: schemas.BasketPydantic,
):
    return await BascketService().update_bascket(
        uow=uow, uuid_id=uuid_id, bascket_update=bascket_update, partial=True
    )


@router.patch(
    "/sign/{uuid_id}/",
    response_model=schemas.BasketPydantic,
    summary="Подписать корзину.",
    description="""
        Принимает в query uuid_id корзины, который сформировал клиентский код. 
        В теле ожидатеся ключ доступа в котором зашифрован ID пользователя, 
        которым и будет подписана корзина.
        """,
)
async def sign_basket(uow: UOF_Depends, uuid_id: str, access_token: TokenSchema):
    basket = await BascketService().sign_basket(
        uow=uow, uuid_id=uuid_id, access_token=access_token
    )
    return basket


# DELETE        === === === === === === === ===
@router.delete(
    "/{uuid_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удали корзину.",
    description="Удалит корзину безвозвратно.",
)
async def delete_bascket(uow: UOF_Depends, uuid_id: str) -> None:
    await BascketService().delete_bascket(uow=uow, uuid_id=uuid_id)


@router.post(
    "/create_or_update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.BasketPydantic,
    summary="Создай или обнови корзину.",
    description="""Создаст новую корзину, если она не существует, 
                или обновит существующию. Из обязательно 'uuid_id' и basket_items 
                не пустой. Если с товаром идет подарок - то указать как 'gift_prod_id'.
                """,
    responses={
        404: {"description": "Сам виноват."},
        500: {"description": "Да пошел ты!"},
    },
    response_description="Информация о корзине.",
)
async def create_or_update_basket(
    new_bascket: schemas.BasketPydantic,
    uow: UOF_Depends,
):
    try:
        uuid_id = new_bascket.uuid_id
        return await BascketService().create_or_update_bascket(
            uow=uow, uuid_id=uuid_id, bascket_data=new_bascket
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ошибка? -> {error!r}.",
        )


@router.patch(
    "/{uuid_id}/{product_id}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.BasketItemUpdate,
    summary="Изменить кол-во продукта в корзине или удалить его из нее.",
    description="""
                Принимает uuid_id корзины и product_id - это параметры для 
                навигации (какой товар хотим удалить/изменить колличество).
                В теле указывается поле count - для изменения кол-ва и поле 
                delete - если истина, то удалит товар с корзины.
                """,
)
async def basket_item_update(
    uow: UOF_Depends,
    uuid_id: str,
    product_id: str,
    data_item: schemas.BasketItemUpdate,
):
    await BascketService().basket_item_update(
        uow,
        uuid_id,
        product_id,
        data_item,
    )
    return data_item
