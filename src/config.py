"""
Configuration module for the AI Currency Converter.

This module centralizes all application configuration,
environment variables, model settings, API configuration,
and application constants.
"""

from dataclasses import dataclass, field
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass(frozen=True)
class EnvironmentConfig:
    """
    Environment variables.
    """

    exchange_rate_url: str = os.getenv("EXCHANGE_RATE_URL", "")
    exchange_rate_api_key: str = os.getenv("EXCHANGE_RATE_API_KEY", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")


@dataclass(frozen=True)
class ModelConfig:
    """
    Gemini model configuration.
    """

    model_name: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    temperature: float = 0.2


@dataclass(frozen=True)
class APIConfig:
    """
    API configuration.
    """

    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))


@dataclass(frozen=True)
class AppConfig:
    """
    Streamlit application configuration.
    """

    app_title: str = "💱 AI Currency Converter"
    app_icon: str = "💱"
    page_layout: str = "centered"

    default_source_currency: str = os.getenv(
        "DEFAULT_SOURCE_CURRENCY",
        "USD",
    )

    default_target_currency: str = os.getenv(
        "DEFAULT_TARGET_CURRENCY",
        "INR",
    )

    supported_currencies: list[str] = field(
        default_factory=lambda: [
            "USD",
            "INR",
            "EUR",
            "GBP",
            "JPY",
            "AUD",
            "CAD",
            "CHF",
            "CNY",
            "SGD",
            "NZD",
            "AED",
            "SAR",
            "PKR",
            "BDT",
            "NPR",
        ]
    )


@dataclass(frozen=True)
class PromptConfig:
    """
    Prompt configuration.
    """

    max_response_tokens: int = 512


class Config:
    """
    Central configuration object.

    Example:
        from src.config import config

        config.env.exchange_rate_url
        config.model.model_name
        config.api.request_timeout
        config.app.supported_currencies
    """

    env = EnvironmentConfig()
    model = ModelConfig()
    api = APIConfig()
    app = AppConfig()
    prompt = PromptConfig()


config = Config()