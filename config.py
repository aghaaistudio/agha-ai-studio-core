"""
Agha AI Studio — Central Configuration

All application settings live here. Values are read from environment
variables (.env file in development, real environment variables in
production). Never hardcode secrets in this file.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# Absolute path of the project directory (where this file lives).
BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration shared by all environments."""

    # Flask core
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

    # Database (SQLite in development; PostgreSQL later in production)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'agha.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # OpenAI (added in a later step)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "")

    # Anthropic Claude (added in a later step)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "")

    # DeepSeek (added in a later step)
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "")

    # Networking
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

    # Environment
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV == "development"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    def __init__(self):
        if self.SECRET_KEY == "dev-only-change-me":
            raise RuntimeError(
                "SECRET_KEY must be set via environment in production."
            )


def get_config():
    """Return the correct config class based on FLASK_ENV."""
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()
