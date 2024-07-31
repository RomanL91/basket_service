import re

from datetime import datetime
from typing import Annotated, List, Dict
from pydantic import BaseModel, ConfigDict, Field


class SimpleMSGErrorPydantic(BaseModel):
    status_code: int
    message: str


class BasketPydantic(BaseModel):
    model_config = ConfigDict(strict=True)

    uuid_id: Annotated[
        str,
        Field(
            ...,
            description="Уникальный ID с клиента",
            examples=["fcff9649-c7cc-498c-8ee2-c84785a68521"],
        ),
    ] = None
    user_id: Annotated[
        int | str | None,
        Field(
            ...,
            description="Уникальный ID пользователя",
            examples=[789],
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
        List[Dict[str, int]] | None,
        Field(
            ...,
            description="Состав корзины",
            example=[
                {
                    "prod_id": 1,
                    "count": 5,
                    "price": 799,
                },
                {
                    "prod_id": 2,
                    "count": 3,
                    "price": 4599,
                },
            ],
        ),
    ] = None
