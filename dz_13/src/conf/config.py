from typing import Any
from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg2://postgres:11111111@localhost:5432/postgres"
    SECRET_KEY_JWT: str = "secret_key"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: EmailStr = "robota_test@meta.ua"
    MAIL_PASSWORD: str = "21061984Polina"
    MAIL_FROM: str = "robota_test@meta.ua"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"
    REDIS_DOMAIN: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = 'postgres'
    CLD_API_KEY: int = 326488457974591
    CLD_API_SECRET: str = "secret"

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v


    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()