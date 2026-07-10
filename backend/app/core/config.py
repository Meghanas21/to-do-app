"""
Centralized application configuration.

WHY THIS FILE EXISTS (fixes CORS root cause #1 — scattered/hardcoded origins):
A very common source of CORS errors is hardcoding allowed origins directly in
main.py, or defining them in more than one place so they drift out of sync.
This module reads configuration from environment variables / .env ONCE and
exposes a single `settings` object that every other module imports. There is
exactly one place that defines which frontend origins are allowed to call
the API.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Todo API"
    ENVIRONMENT: str = "development"

    # --- CORS ---
    # Stored as a raw comma-separated string in .env, parsed into a list below.
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- JWT / Auth ---
    SECRET_KEY: str = "insecure-dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- Database ---
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/knowledge_db"

    # --- Seed data ---
    DEFAULT_ADMIN_EMAIL: str = "admin@example.com"
    DEFAULT_ADMIN_PASSWORD: str = "Admin123!"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Turn 'http://localhost:5173,http://127.0.0.1:5173' into a clean list.

        Trailing slashes are stripped because 'http://localhost:5173/' and
        'http://localhost:5173' are treated as DIFFERENT origins by browsers,
        and CORSMiddleware does exact string matching. A stray trailing slash
        is a classic silent cause of "works in Postman, fails in browser".
        """
        return [origin.strip().rstrip("/") for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
