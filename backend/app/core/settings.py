from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MouseIA"
    app_environment: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./data/mouseia.db"
    jwt_secret_key: str = "dev-secret-key-change-me-in-production"
    gemini_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
