from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    REFRESH_TOKRN_EXPIRE_DAYS: int
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        # Load the env file located alongside this module
        env_file=Path(__file__).resolve().parent / ".env",
        extra="ignore")

Config = Settings()
