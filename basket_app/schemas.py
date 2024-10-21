from enum import Enum
from typing import Annotated, Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field


# Определение этапов оформления
class CheckoutStageSchema(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"


class SimpleMSGErrorPydantic(BaseModel):
    status_code: int
    message: str


class BasketPydantic(BaseModel):
    model_config = ConfigDict(
        strict=True,
        json_schema_extra={
            "example": {
                "uuid_id": "fcff9649-c7cc-498c-8ee2-c84785a68521",
                "basket_items": [
                    {
                        "prod_id": 1,
                        "count": 5,
                        "price": 799,
                    },
                    {
                        "prod_id": 2,
                        "count": 3,
                        "price": 4599,
                        "gift_prod_id": 1,
                    },
                ],
                # gift_items не включается в пример
            }
        },
    )

    uuid_id: Annotated[
        str,
        Field(
            ...,
            description="Уникальный ID с клиента",
        ),
    ] = None
    user_id: Annotated[
        Optional[str],
        Field(
            str,
            description="Уникальный ID пользователя",
        ),
    ] = None
    completed: Annotated[
        bool | None,
        Field(
            ...,
            description="Статус корзины",
            examples=[False],
        ),
    ] = False
    basket_items: Annotated[
        # TODO улучшить аннотацию
        List[Dict[str, str | int | dict | list]] | None,
        Field(
            ...,
            description="Состав корзины",
        ),
    ] = None
    gift_items: Annotated[
        # TODO улучшить аннотацию
        List[Dict[str, str | int | Dict | List | None]] | None,
        Field(
            ...,
            description="Список подарков",
        ),
    ] = None


class BasketItemUpdate(BaseModel):
    model_config = ConfigDict(
        strict=True,
    )

    count: Annotated[
        int,
        Field(
            ...,
            # description=
        ),
    ]
    delete: Annotated[
        bool,
        Field(
            ...,
            # description=
        ),
    ] = False
