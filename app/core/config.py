from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "releaseguard"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "local"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()