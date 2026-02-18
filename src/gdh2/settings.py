from __future__ import annotations

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# Garantimos carregamento do .env em dev/test (Flask 3 não carrega automaticamente em todos os casos).
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ENV: str = "development"
    SECRET_KEY: str = "change-me"

    # Default facilita bootstrap e testes; em produção, sobrescreva via env.
    DATABASE_URL: str = "postgresql+psycopg://gdh2:gdh2@localhost:5432/gdh2"


settings = Settings()
