from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING, List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL

DIR = Path(__file__).absolute().parent.parent.parent
BOT_DIR = Path(__file__).absolute().parent.parent


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="bot/.env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter=","       #
    )


class WebhookSettings(EnvBaseSettings):
    USE_WEBHOOK: bool
    WEBHOOK_BASE_URL: str
    WEBHOOK_PATH: str 
    WEBHOOK_SECRET: str 
    WEBHOOK_HOST: str
    WEBHOOK_PORT: int = 8080

    @property
    def webhook_url(self) -> str:
        if settings.USE_WEBHOOK:
            return f"{self.WEBHOOK_BASE_URL}{self.WEBHOOK_PATH}"
        return f"http://localhost:{settings.WEBHOOK_PORT}{settings.WEBHOOK_PATH}"


class BotSettings(EnvBaseSettings):
    BOT_TOKEN: str
    YANDEX_API_KEY: str
    YANDEX_FOLDER_ID: str
    ML_SERVER_URL: str

    # Обратите внимание: поле должно быть именно так написано,
    # чтобы совпадало с ENV-переменной ADMIN_IDS
    ADMIN_IDS: str

    # @field_validator("ADMIN_IDS", mode="before")
    # @classmethod
    # def _parse_admin_ids(cls, v):
    #     # если пришла строка, распарсим по запятой
    #     if isinstance(v, str):
    #         return [int(item) for item in v.split(",") if item.strip()]
    #     # иначе оставляем как есть (например, уже List[int])
    #     return v

class CacheSettings(EnvBaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_USER: str | None = None

    # REDIS_DATABASE: int = 1
    # REDIS_TTL_STATE: int | None = None
    # REDIS_TTL_DATA: int | None = None

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"





class Settings(BotSettings, CacheSettings, WebhookSettings):
    DEBUG: bool = False

    SENTRY_DSN: str | None = None




settings = Settings()
