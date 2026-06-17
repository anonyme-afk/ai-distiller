"""
settings.py
Centralized configuration loaded from environment variables / .env file.
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    brave_api_key: str | None = None
    tavily_api_key: str | None = None
    hf_token: str | None = None

    default_teacher: str = "claude-3-5-sonnet-20241022"
    default_domain: str = "general"
    cache_dir: str = "./cache"
    output_dir: str = "./outputs"


def get_settings() -> Settings:
    return Settings()
