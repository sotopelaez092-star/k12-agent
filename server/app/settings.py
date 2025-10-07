from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    app_name: str = "k12-agent"
    log_level:str = "INFO"
    host: str = "127.0.0.1"
    port: int = 8001
    env: str = "dev"
    version: str = "0.1.0"
    cors_allow_origins: List[str] = ["*"]
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    cors_expose_headers: List[str] = ["X-Request-ID"]
    cors_allow_credentials: bool = False
    # 从 .env 读取，支持 APP_ 前缀的环境变量
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
    )

# 实例化 Settings 类，用于在应用中获取配置
settings = Settings()