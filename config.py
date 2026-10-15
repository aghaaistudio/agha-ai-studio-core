"""
Agha AI Studio — Central Configuration

All application settings live here. Values are read from environment
variables (.env file in development, real environment variables in
production). Never hardcode secrets in this file.
"""
import os
from dotenv import load_dotenv

# Load .env file if present (development convenience).
# In production, environment variables are set by the host.
load_dotenv()


class Config:
    """Base configuration shared by all environments."""

    # ------------------------------------------------------------------
    # Flask core
    # ------------------------------------------------------------------
    # In production, SECRET_KEY MUST be set via environment variable.
    # This default is only safe for local development.
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

    # ------------------------------------------------------------------
    # Google Gemini
    # ------------------------------------------------------------------
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # ------------------------------------------------------------------
    # OpenAI (added in a later step)
    # ------------------------------------------------------------------
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "")

    # ------------------------------------------------------------------
    # Anthropic Claude (added in a later step)
    # ------------------------------------------------------------------
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "")

    # ------------------------------------------------------------------
    # DeepSeek (added in a later step)
    # ------------------------------------------------------------------
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "")

    # ------------------------------------------------------------------
    # Networking
    # ------------------------------------------------------------------
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

    # ------------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------------
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV == "development"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Production requires an explicit SECRET_KEY — refuse a weak default.
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
