import logging
from enum import Enum

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class TgBotConfig(BaseModel):
    token: str
    admin_ids: list[int] | None = None
    register_passphrase: str | None = None


class DatabaseConfig(BaseModel):
    driver: str = "asyncpg"
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str
    database: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    def construct_url(
        self,
        driver: str | None = None,
        host: str | None = None,
        port: int | None = None,
    ) -> str:
        driver = driver or self.driver
        host = host or self.host
        port = port or self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: str | None = None
    database: int = 0

    def dsn(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.database}"
        return f"redis://{self.host}:{self.port}/{self.database}"


class Envs(Enum):
    local_test = "local_test"
    stage = "stage"
    prod = "prod"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env",),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )

    tg_bot: TgBotConfig = Field(default_factory=TgBotConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)

    environment: Envs = Envs.local_test
    logging_level: int = logging.INFO

    inline_kb_button_row_width: int = 2
    schedule_healthcheck: str = Field(
        default="7:00",
        description="Time of daily healthcheck in HH:MM format",
    )


config = Config()
