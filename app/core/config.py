import re
from datetime import timedelta
from functools import lru_cache
from typing import Any

from pydantic import field_validator
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

    TTL_CACHE_EXTERNAL_API: timedelta = timedelta(seconds=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @field_validator('TTL_CACHE_EXTERNAL_API', mode='plain')
    @classmethod
    def is_ttl_cache_external_api(cls, value: Any) -> timedelta:
        if isinstance(value, timedelta):
            return value
        if not isinstance(value, str):
            raise ValueError(f'{value} is not valide type, must be string')
        pattern = "(^\d*)([s,m,h,d]$)"
        r = re.compile(pattern)
        m = r.match(value)
        if m:
            v = float(m[1])
            match m[2]:
                case 's':
                    return timedelta(seconds=v)
                case 'm':
                    return timedelta(minutes=v)
                case 'h':
                    return timedelta(hours=v)
                case 'd':
                    return timedelta(days=v)
        raise ValueError(f'{value} is not valide')


@lru_cache
def get_settings():
    return Settings()
