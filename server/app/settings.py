from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "k12-agent"
    log_level:str = "INFO"
    host: str = "127.0.0.1"
    port: int = 8001

    # 从 .env 读取，支持 APP_ 前缀的环境变量
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
    )

# 实例化 Settings 类，用于在应用中获取配置
settings = Settings()