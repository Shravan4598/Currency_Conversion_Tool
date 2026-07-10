"""
Utility functions for the AI Currency Converter application.
"""

from __future__ import annotations

import re
import sys
from typing import Any

from src.exception import ConversionException
from src.logger import logging


class CurrencyUtils:
    """
    Utility class containing helper methods for
    currency conversion operations.
    """

    # ISO-4217 currency code format
    CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")

    @staticmethod
    def validate_amount(amount: float) -> None:
        """
        Validate the currency amount.

        Args:
            amount (float): Amount entered by the user.

        Raises:
            ConversionException: If amount is invalid.
        """
        try:
            if amount is None:
                raise ValueError("Amount cannot be empty.")

            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

        except Exception as e:
            logging.error(str(e))
            raise ConversionException(e, sys)

    @staticmethod
    def validate_currency(currency: str) -> str:
        """
        Validate ISO currency code.

        Args:
            currency (str): Currency code.

        Returns:
            str: Uppercase validated currency code.

        Raises:
            ConversionException: If currency code is invalid.
        """
        try:
            if not currency:
                raise ValueError("Currency cannot be empty.")

            currency = currency.strip().upper()

            if not CurrencyUtils.CURRENCY_PATTERN.match(currency):
                raise ValueError(
                    "Currency code must contain exactly 3 alphabetic characters."
                )

            return currency

        except Exception as e:
            logging.error(str(e))
            raise ConversionException(e, sys)

    @staticmethod
    def format_currency(value: float) -> str:
        """
        Format a numeric value with commas.

        Example:
            123456.789 -> 123,456.79
        """
        return f"{value:,.2f}"

    @staticmethod
    def build_conversion_result(
        amount: float,
        source_currency: str,
        target_currency: str,
        exchange_rate: float,
        converted_amount: float,
        explanation: str,
    ) -> dict[str, Any]:
        """
        Create the final response dictionary.

        Returns:
            dict
        """
        return {
            "amount": amount,
            "source_currency": source_currency,
            "target_currency": target_currency,
            "exchange_rate": exchange_rate,
            "converted_amount": converted_amount,
            "formatted_result": (
                f"{CurrencyUtils.format_currency(amount)} "
                f"{source_currency} = "
                f"{CurrencyUtils.format_currency(converted_amount)} "
                f"{target_currency}"
            ),
            "explanation": explanation,
        }

    @staticmethod
    def safe_float(value: Any) -> float:
        """
        Safely convert any numeric value to float.

        Args:
            value: Value to convert.

        Returns:
            float

        Raises:
            ConversionException
        """
        try:
            return float(value)

        except Exception as e:
            logging.error(str(e))
            raise ConversionException(e, sys)