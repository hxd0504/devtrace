from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "DevTrace"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时

    class Config:
        env_file = ".env"


settings = Settings()
