from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Uses python-dotenv through pydantic-settings (shipped with fastapi[standard]).
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: str = Field(default="", validation_alias="SECRET_KEY")
    debug: bool = Field(default=False, validation_alias="DEBUG")

    ridwaanhall_main_api: str = Field(
        default="",
        validation_alias="RIDWAANHALL_MAIN_API",
    )
    api_key: str = Field(default="", validation_alias="API_KEY")

    ridwaanhall_api_x: str = Field(default="Host", validation_alias="RIDWAANHALL_API_X")
    ridwaanhall_x: str = Field(default="Origin", validation_alias="RIDWAANHALL_X")
    ridwaanhall_hash_x: str = Field(
        default="", validation_alias="RIDWAANHALL_HASH_X"
    )

    ridwaanhall_api_key: str = Field(
        default="", validation_alias="RIDWAANHALL_API_KEY"
    )
    ridwaanhall_key: str = Field(default="", validation_alias="RIDWAANHALL_KEY")
    ridwaanhall_hash_key: str = Field(
        default="", validation_alias="RIDWAANHALL_HASH_KEY"
    )

    api_availability: bool = Field(default=True, validation_alias="API_AVAILABILITY")
    api_version: str = Field(default="4.0.0", validation_alias="API_VERSION")
    last_update: str = Field(
        default="2026-05-29T00:00:00+07:00",
        validation_alias="LAST_UPDATE",
    )
    api_timeout: int = Field(default=8, validation_alias="API_TIMEOUT")


@lru_cache
def get_settings() -> Settings:
    return Settings()
