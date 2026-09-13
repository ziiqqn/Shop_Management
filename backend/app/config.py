from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3307
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "shop_db"

    # JWT 配置
    JWT_SECRET: str = "default-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
