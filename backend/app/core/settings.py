from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MouseIA"
    app_environment: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./mouseia.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
