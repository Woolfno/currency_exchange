from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    db_host: str = "localhost"
    db_port: str = "5432"
    db_user: str = ""
    db_pass: str = ""
    db_name: str = ""

    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


@lru_cache
def get_settings():
    return Settings()
