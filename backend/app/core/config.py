from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Army Asset Lifecycle Management System"
    VERSION: str = "1.0.0"

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()