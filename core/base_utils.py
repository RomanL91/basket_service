import jwt

import httpx

from decimal import Decimal

from collections import Counter

from core.settings import settings


def check_token(jwt_value: str) -> bool:
    try:
        payload_data = jwt.decode(
            jwt_value,
            settings.auth_jwt.public_key,
            settings.auth_jwt.algorithm,
        )
        if payload_data["type"] != settings.auth_jwt.allowed_key_type:
            return False
        return payload_data
    except:
        return False


def get_total_sum_per_basket(shipping_city: str, basket_items: list) -> Decimal:
    total_amount_to_order = []
    try:
        prod_with_count = dict(Counter(basket_items))
        params = {"ids": ",".join(map(str, basket_items)), "city": shipping_city}
        url = settings.api_shop.get_prod_by_ids()
        response = httpx.get(url, params=params)
        response.raise_for_status()
        response_data = response.json()
        products = response_data.get("results", None)

        if products is None:
            raise ValueError("В данном городе нет этого товара.")
        for el in products:
            count = prod_with_count.get(el["id"], 0)
            price = Decimal(el.get("stocks").get(shipping_city).get("price"))
            total_amount_to_pos = price * count
            total_amount_to_order.append(total_amount_to_pos)
        total_sum = sum(total_amount_to_order)

        # return Decimal(100)
        return Decimal(total_sum)
    except (KeyError, TypeError) as e:
        raise ValueError("Нарушение структуры корзины.")
    except httpx.ConnectError:
        raise ValueError("Нет ответа от сервиса.")
