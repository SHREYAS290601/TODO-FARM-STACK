from pydantic_settings import BaseSettings
from decouple import config
from pydantic import AnyHttpUrl
from typing import List, Annotated, Tuple, Union


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    MONGODB_CONNECTION_STRING: str = config("MONGODB_CONNECTION_STRING", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 75
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    PROJECT_NAME: str = "Lets-Do"

    class Config:
        case_sensitive = True


settings = Settings()
