import urllib.parse
from functools import lru_cache

from dotenv import find_dotenv
from pydantic import PostgresDsn, model_validator
from pydantic.types import PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    """Base settings for all settings."""

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        arbitrary_types_allowed=True,
        case_sensitive=True,
        env_nested_delimiter="__",
        coerce_numbers_to_str=True,
        extra="ignore",
    )


class BotSettings(_Settings):

    BOT_TOKEN: str = "token"


class Postgresql(_Settings):
    """Postgresql settings."""

    #: str: Postgresql host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of postgresql.
    PORT: PositiveInt = 5432
    #: str: Postgresql user.
    USER: str = "postgresql"
    #: SecretStr: Postgresql password.
    PASSWORD: SecretStr = SecretStr("postgresql")
    #: str: Postgresql database name.
    DATABASE_NAME: str = "postgresql"

    #: PositiveInt: Min count of connections in one pool to postgresql.
    MIN_CONNECTION: PositiveInt = 1
    #: PositiveInt: Max count of connections in one pool  to postgresql.
    MAX_CONNECTION: PositiveInt = 16

    #: str: Concatenation all settings for postgresql in one string. (DSN)
    #  Builds in `root_validator` method.
    DSN: str | None = None

    TEST_DSN: str | None = None

    @model_validator(mode="before")
    @classmethod
    def build_dsn(cls, data: dict) -> dict:
        """Build DSNs for async SQLAlchemy (postgresql+asyncpg)."""

        password = urllib.parse.quote_plus(data.get("PASSWORD"))

        data["DSN"] = str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=data.get("USER"),
                password=password,
                host=data.get("HOST"),
                port=int(data.get("PORT")),
                path=f"{data.get('DATABASE_NAME')}",
            ),
        )

        data["TEST_DSN"] = str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=data.get("USER"),
                password=password,
                host=data.get("HOST"),
                port=int(data.get("PORT")),
                path=f"test_{data.get('DATABASE_NAME')}",
            ),
        )

        return data


class Settings(_Settings):

    POSTGRES: Postgresql

    BotSettings: BotSettings


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
