from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 数据库配置（允许空值，由代码兜底）
    DB_HOST: str = "localhost"
    DB_PORT: Optional[int] = 3306
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 处理空字符串：如果环境变量是空串，就用默认值
        if self.DB_PORT is None or str(self.DB_PORT).strip() == "":
            self.DB_PORT = 3306
        if not self.DB_HOST or self.DB_HOST.strip() == "":
            self.DB_HOST = "localhost"
        if not self.DB_USER or self.DB_USER.strip() == "":
            self.DB_USER = "root"
        if not self.DB_NAME or self.DB_NAME.strip() == "":
            self.DB_NAME = "shop_db"


settings = Settings()