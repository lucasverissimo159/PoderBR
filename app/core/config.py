from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "PoderBR"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Defaults to SQLite for local development
    DATABASE_URL: str = "sqlite:///./poderbr.db"

    @property
    def cors_origins_list(self) -> list[str]:
        if isinstance(self.CORS_ORIGINS, str):
            return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]
        return self.CORS_ORIGINS

    CORS_ORIGINS: list[str] | str = ["*"]
    RATE_LIMIT_DEFAULT: str = "100/minute"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
