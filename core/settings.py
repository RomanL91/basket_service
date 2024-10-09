from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from fastapi.middleware.cors import CORSMiddleware


BASE_DIR = Path(__file__).parent.parent


class SettingsDataBase(BaseModel):
    # for example "postgresql://user:password@localhost/dbname"
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # docker url
    # url: str = (
    #     "postgresql+asyncpg://MyBasketUser:MyBasketPassword@postgres:5432/MyBasketDataBase"
    # )
    # local url
    # url: str = (
    #     "postgresql+asyncpg://MyBasketUser:MyBasketPassword@localhost:5433/MyBasketDataBase"
    # )
    echo: bool = True  # Для дебага
    future: bool = True


class SettingsAuth(BaseModel):
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    public_key: str = public_key_path.read_text()
    algorithm: str = "RS256"
    allowed_key_type: str = "access_token"


class SettingsCORSMiddleware(BaseModel):
    origins: list[str] = ["http://localhost", "http://localhost:3000"]
    middleware: dict = {
        "middleware_class": CORSMiddleware,
        "allow_origins": origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }


class SettingsApiShop(BaseModel):
    host_addr_api: str = "http://127.0.0.1:8000/"
    prod_by_ids_template: str = "{host}api/v1/products/by_ids/{prod_ids_str}/"
    url_admin_prod_detail: str = "{host}admin/app_products/products/{prod_id}/change/"
    url_api_prod_detail: str = "{host}api/v1/products/{prod_slug}/"

    def _format_url(self, template: str, **kwargs) -> str:
        defaults = {"host": self.host_addr_api}
        data = {**defaults, **kwargs}
        return template.format(**data)

    def get_prod_by_ids(self, **kwargs):
        return self._format_url(self.prod_by_ids_template, **kwargs)

    def get_url_admin_prod_detail(self, **kwargs):
        return self._format_url(self.url_admin_prod_detail, **kwargs)

    def get_url_api_prod_detail(self, **kwargs):
        return self._format_url(self.url_api_prod_detail, **kwargs)


class Settings(BaseSettings):
    # == start app
    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8989
    reload_flag: bool = True

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


settings = Settings()
