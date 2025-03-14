from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

from httpx import Request, AsyncClient, HTTPError

from core import settings


# Интерфейс для обработчиков типов данных
class RequestHandler(ABC):
    @abstractmethod
    def prepare_request(
        self, url: str, headers: dict = None, data: dict = None
    ) -> Request:
        pass


# Обработчик для JSON
class JsonRequestHandler(RequestHandler):
    def prepare_request(
        self, url: str, headers: dict = None, data: dict = None
    ) -> Request:
        request = Request(method="POST", url=url, headers=headers, json=data)
        if headers is not None:
            request.headers.update(headers)
        request.headers["Content-Type"] = "application/json"
        return request


# Обработчик для Form URL Encoded
class FormUrlEncodedRequestHandler(RequestHandler):
    def prepare_request(
        self, url: str, headers: dict = None, data: dict = None
    ) -> Request:
        request = Request(method="POST", url=url, headers=headers, data=data)
        request.headers["Content-Type"] = "application/x-www-form-urlencoded"
        return request


class ApiPayBank:
    auth_url = settings.api_bank.auth_url
    pay_link_url = settings.api_bank.pay_link_url

    @dataclass
    class TokenAtr:
        # для получения токена
        grant_type: str = settings.api_bank.grant_type
        scope: str = settings.api_bank.scope
        username: str = settings.api_bank.username
        password: str = settings.api_bank.password
        client_id: str = settings.api_bank.client_id
        client_secret: str = settings.api_bank.client_secret

    @dataclass
    class AuthorizationHeader:
        Authorization: str

        def __init__(self, token: str):
            self.Authorization = f"Bearer {token}"

    @dataclass
    class JsonPayload:
        # динамичные параметры, передаются как аргументы для создания экземпляра
        invoice_id: str  # "809"
        amount: int  # 1500
        description: str  # "тест деск"
        recipient_contact: str  # "djasaram@gmail.com"
        recipient_contact_sms: str  # "+77714648717"
        notifier_contact_sms: str  # "+77714648717"
        # статичные параметры для выноса в файл настроек -> файл окружения
        shop_id: str = settings.api_bank.shop_id
        account_id: str = settings.api_bank.account_id
        language: str = settings.api_bank.language
        expire_period: str = settings.api_bank._expire_period
        currency: str = settings.api_bank.currency
        post_link: str = settings.api_bank.post_link
        failure_post_link: str = settings.api_bank.failure_post_link
        back_link: str = settings.api_bank.back_link
        failure_back_link: str = settings.api_bank.failure_back_link

    @classmethod
    async def _post_request(cls, url, data, handler: RequestHandler, headers=None):
        headers = headers or {}
        request = handler.prepare_request(url, headers, data)
        async with AsyncClient() as client:
            try:
                response = await client.send(request)

                # ВРЕМЕННО: печатаем статус и текст ответа
                print(f"[DEBUG] Bank response status: {response.status_code}")
                print(f"[DEBUG] Bank response text: {response.text!r}")

                return response.json()
            except HTTPError as e:
                raise ValueError(f"Что же пошло не так..: {str(e)}")

    @classmethod
    async def get_token(cls):
        payload_data = asdict(cls.TokenAtr())
        response_data = await cls._post_request(
            url=cls.auth_url, data=payload_data, handler=FormUrlEncodedRequestHandler()
        )
        print(f"--- [DEBUG] --- response_data --- > {response_data}")
        token = response_data.get("access_token")
        if not token:
            raise ValueError("Нет ключа доступа для проведения оплаты.")
        return token

    @classmethod
    async def create_payment_link(cls, **data):
        token = await cls.get_token()
        authorization_headers = asdict(cls.AuthorizationHeader(token))
        payload_data = asdict(cls.JsonPayload(**data))
        response_data = await cls._post_request(
            url=cls.pay_link_url,
            data=payload_data,
            headers=authorization_headers,
            handler=JsonRequestHandler(),
        )
        return response_data.get("invoice_url")
