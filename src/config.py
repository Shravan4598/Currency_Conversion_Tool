"""
Configuration module for the AI Currency Converter application.

This module centralizes all application configuration, environment
variables, API endpoints, model configuration, and application constants.
"""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


@dataclass(frozen=True)
class EnvironmentConfig:
    """
    Stores all environment variables required by the application.
    """

    exchange_rate_url: str = os.getenv("EXCHANGE_RATE_URL", "")
    exchange_rate_api_key: str = os.getenv("EXCHANGE_RATE_API_KEY", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")


@dataclass(frozen=True)
class ModelConfig:
    """
    Configuration for the Gemini model.
    """

    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.2


@dataclass(frozen=True)
class APIConfig:
    """
    API request configuration.
    """

    request_timeout: int = 30
    max_retries: int = 3


@dataclass(frozen=True)
class AppConfig:
    """
    Streamlit application configuration.
    """

    app_title: str = "💱 AI Currency Converter"
    app_icon: str = "💱"

    default_source_currency: str = "USD"
    default_target_currency: str = "INR"

    page_layout: str = "centered"


@dataclass(frozen=True)
class PromptConfig:
    """
    Prompt-related configuration.
    """

    max_response_tokens: int = 512


class Config:
    """
    Central configuration object.

    Usage:
        from src.config import config

        config.env.exchange_rate_url
        config.model.model_name
        config.api.request_timeout
    """

    env = EnvironmentConfig()
    model = ModelConfig()
    api = APIConfig()
    app = AppConfig()
    prompt = PromptConfig()


config = Config()