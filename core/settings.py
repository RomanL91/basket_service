import os
from pathlib import Path
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings

from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).parent.parent
load_dotenv(".env")


class SettingsDataBase(BaseModel):
    # for example "postgresql://user:password@localhost/dbname"
    # url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # docker url
    # url: str = (
    #     "postgresql+asyncpg://MyBasketUser:MyBasketPassword@postgres:5432/MyBasketDataBase"
    # )
    # local url
    url: str = os.getenv("DATABASE_URL")
    echo: bool = True  # Для дебага
    future: bool = True


class SettingsAuth(BaseModel):
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    public_key: str = public_key_path.read_text()
    algorithm: str = "RS256"
    allowed_key_type: str = "access_token"


class SettingsCORSMiddleware(BaseModel):
    origins: list[HttpUrl] = ["http://localhost", "http://localhost:3000"]
    middleware: dict = {
        "middleware_class": CORSMiddleware,
        "allow_origins": origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }


class SettingsApiShop(BaseModel):
    host_addr_api: HttpUrl = os.getenv("HOST_ADDR_API")
    prod_by_ids_template: HttpUrl = "{host}api/v2/products_v2/filter_by_ids/"
    url_admin_prod_detail: HttpUrl = (
        "{host}admin/app_products/products/{prod_id}/change/"
    )
    url_api_prod_detail: HttpUrl = "{host}api/v1/products/{prod_slug}/"

    def _format_url(self, template: str, **kwargs) -> HttpUrl:
        defaults = {"host": self.host_addr_api}
        data = {**defaults, **kwargs}
        return template.format(**data)

    def get_prod_by_ids(self, **kwargs):
        return self._format_url(self.prod_by_ids_template, **kwargs)

    def get_url_admin_prod_detail(self, **kwargs):
        return self._format_url(self.url_admin_prod_detail, **kwargs)

    def get_url_api_prod_detail(self, **kwargs):
        return self._format_url(self.url_api_prod_detail, **kwargs)


class SettingsApiBank(BaseModel):
    # =================================================================
    # ссылки на которых "завязана" логика получения платежной ссылки
    auth_url: HttpUrl = os.getenv("AUTH_URL")
    pay_link_url: HttpUrl = os.getenv("PAY_LINK_URL")

    # =================================================================
    # данные для получения токена доступа от банка
    grant_type: str = (
        "password"  # тип авторизации, для проведения платежа используется тип client_credentials (а тут password...)
    )
    scope: str = (
        "webapi usermanagement email_send verification statement statistics payment"  # ресурс
    )
    username: str = os.getenv("USERNAMEAPI")
    password: str = os.getenv("PASSWORD")
    client_id: str = os.getenv("CLIENT_ID")
    client_secret: str = os.getenv("CLIENT_SECRET")

    # =================================================================
    # статическая часть данных для "полезной нагрузки" для получения конкретной ссылки на оплату
    # --->> ID магазина, выдается системой при регистрации магазина, обязательное
    shop_id: str = os.getenv("SHOP_ID")
    # --->> номер счета магазина в системе epay, генериурется коммерсантом, обязательное
    account_id: str = "92771601"
    # --->> язык, на котором должна быть представлена информация о счете (допустимые значения: "rus", "kaz", "eng"), обязательное
    language: str = "rus"
    # --->> период действия счета. Формат: "[число][единица времени]", где единица времени может принимать значение "d" (дни). Например, "2d" - счет действителен в течение двух дней, обязательное
    _expire_period: str = os.getenv("EXPIRE_PERIOD")

    @property
    def expire_period(self):
        return int(self._expire_period[:1])

    # --->> валюта счета (допустимые значения: "KZT"), обязательное
    currency: str = "KZT"
    # --->> URL-адрес, на который будет отправлен POST-запрос после успешной оплаты счета.
    post_link: HttpUrl = os.getenv("POST_LINK")
    # --->> URL-адрес, на который будет отправлен POST-запрос в случае неуспешной оплаты счета.
    failure_post_link: HttpUrl = os.getenv("FAIURE_POST_LINK")
    # --->> Ссылка для возврата в магазин при удачном платеже.
    back_link: HttpUrl = os.getenv("BACK_LINK")
    # --->> Ссылка для возврата в магазин при неудачном платеже.
    failure_back_link: HttpUrl = os.getenv("FAILURE_BACK_LINK")

    # =================================================================
    # ссылка для редиректа в случае если пользователь выбрал "оплата при получении"
    # --->> Ссылка для возврата в магазин если пользователь выбрал "наличный" способ.
    self_link_order_dateil: HttpUrl = os.getenv("SELF_LINK_ORDER_DETAIL")
    # --->> Ссылка на страницу, если в ответе от банка нет "invoice_url" для редиректа на платежную страницу.
    self_link_redirect_not_successful: HttpUrl = "http://example.com/"


class Settings(BaseSettings):
    # == start app
    app: str = "main:app"
    host: str = os.getenv("HOST")
    port: int = os.getenv("PORT")
    reload_flag: bool = os.getenv("RELOAD")

    # == other
    api_v1_prefix: str = "/basket_api/v1"
    time_zone: ZoneInfo = ZoneInfo("Asia/Almaty")

    # == DataBase
    db: SettingsDataBase = SettingsDataBase()
    # == Auth
    auth_jwt: SettingsAuth = SettingsAuth()
    # == CORSMiddleware
    middleware: SettingsCORSMiddleware = SettingsCORSMiddleware()
    # == ApiShop
    api_shop: SettingsApiShop = SettingsApiShop()
    # == ApiBank
    api_bank: SettingsApiBank = SettingsApiBank()


settings = Settings()
