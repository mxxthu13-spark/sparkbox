from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./sparkbox.db"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # AI 模型配置
    DEFAULT_AI_PROVIDER: str = "deepseek"
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    QWEN_API_KEY: Optional[str] = None
    QWEN_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    QWEN_MODEL: str = "qwen-turbo"

    # 对象存储
    OSS_TYPE: str = "local"
    COS_SECRET_ID: Optional[str] = None
    COS_SECRET_KEY: Optional[str] = None
    COS_BUCKET: Optional[str] = None
    COS_REGION: str = "ap-shanghai"

    # 应用配置
    APP_NAME: str = "SparkBox 闪念盒子"
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
