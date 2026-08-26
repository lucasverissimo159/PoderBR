from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "PoderBR"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Defaults to SQLite for local development
    DATABASE_URL: str = "sqlite:///./poderbr.db"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
