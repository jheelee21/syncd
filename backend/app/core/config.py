from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "syncd"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/syncd"

    # JWT
    SECRET_KEY: str = "changethissecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"


settings = Settings()
