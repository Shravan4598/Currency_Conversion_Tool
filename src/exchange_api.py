"""
Exchange Rate API service.

This module communicates with the Exchange Rate API
to fetch live exchange rates.
"""

from __future__ import annotations

import sys
from typing import Dict

import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from src.config import config
from src.exception import ConversionException
from src.logger import logging


class ExchangeRateService:
    """
    Service class for interacting with the Exchange Rate API.
    """

    def __init__(self) -> None:
        self.base_url = config.env.exchange_rate_url
        self.api_key = config.env.exchange_rate_api_key
        self.timeout = config.api.request_timeout

    @retry(
        stop=stop_after_attempt(config.api.max_retries),
        wait=wait_fixed(2),
        reraise=True,
    )
    def _make_request(
        self,
        base_currency: str,
        target_currency: str,
    ) -> Dict:
        """
        Make a request to the Exchange Rate API.

        Args:
            base_currency: Source currency.
            target_currency: Target currency.

        Returns:
            API response as dictionary.

        Raises:
            ConversionException
        """
        try:
            url = (
                f"{self.base_url}/"
                f"{self.api_key}/pair/"
                f"{base_currency}/"
                f"{target_currency}"
            )

            logging.info(
                "Fetching exchange rate: %s -> %s",
                base_currency,
                target_currency,
            )

            response = requests.get(
                url=url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        except Exception as e:
            logging.error(
                "Exchange Rate API request failed: %s",
                str(e),
            )
            raise ConversionException(e, sys)

    @staticmethod
    def _validate_response(data: Dict) -> None:
        """
        Validate API response.

        Args:
            data: API response.

        Raises:
            ConversionException
        """
        try:
            if not data:
                raise ValueError("Empty API response.")

            if data.get("result") != "success":
                raise ValueError(
                    data.get(
                        "error-type",
                        "Exchange Rate API returned an error.",
                    )
                )

            if "conversion_rate" not in data:
                raise ValueError(
                    "Conversion rate not found in API response."
                )

        except Exception as e:
            logging.error(str(e))
            raise ConversionException(e, sys)

    def get_conversion_rate(
        self,
        source_currency: str,
        target_currency: str,
    ) -> float:
        """
        Fetch exchange rate between two currencies.

        Args:
            source_currency: Source currency.
            target_currency: Target currency.

        Returns:
            Exchange rate.

        Raises:
            ConversionException
        """
        try:
            data = self._make_request(
                base_currency=source_currency,
                target_currency=target_currency,
            )

            self._validate_response(data)

            exchange_rate = float(data["conversion_rate"])

            logging.info(
                "Exchange rate fetched successfully: %s -> %s = %.6f",
                source_currency,
                target_currency,
                exchange_rate,
            )

            return exchange_rate

        except Exception as e:
            logging.error(
                "Failed to fetch exchange rate: %s",
                str(e),
            )
            raise ConversionException(e, sys)