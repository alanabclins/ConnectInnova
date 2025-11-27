import secrets
from typing import Literal

from pydantic import AnyHttpUrl, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: Literal["development", "test", "production"] = "development"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    PROJECT_NAME: str
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # database configurations
    MONGO_URI: str
    MONGO_DB: str

    # SSO ID and Secrets
    GOOGLE_CLIENT_ID: str | None = None
    GEMINI_API_KEY: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    SSO_CALLBACK_HOSTNAME: str | None = None
    SSO_LOGIN_CALLBACK_URL: str | None = None

    # EMAILS Settings
    MAIL_USERNAME: str = "user@example.com"
    MAIL_PASSWORD: str = "password"
    MAIL_FROM: str = "user@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    FRONTEND_URL: str = "http://localhost:5173/"

settings = Settings()  # type: ignore
