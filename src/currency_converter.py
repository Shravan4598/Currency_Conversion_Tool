"""
Currency conversion service.

This module contains the business logic responsible for
performing currency conversion calculations.
"""

from __future__ import annotations

import sys

from src.exception import ConversionException
from src.logger import logging


class CurrencyConverter:
    """
    Service responsible for performing currency conversion.

    This class performs only mathematical calculations.
    It does not communicate with external APIs.
    """

    @staticmethod
    def convert(
        amount: float,
        exchange_rate: float,
    ) -> float:
        """
        Convert an amount using the supplied exchange rate.

        Args:
            amount: Source currency amount.
            exchange_rate: Exchange rate.

        Returns:
            Converted amount.

        Raises:
            ConversionException: If the calculation fails.
        """
        try:
            converted_amount = round(amount * exchange_rate, 2)

            logging.info(
                "Currency converted successfully: %.2f × %.6f = %.2f",
                amount,
                exchange_rate,
                converted_amount,
            )

            return converted_amount

        except Exception as e:
            logging.error(
                "Currency conversion failed: %s",
                str(e),
            )
            raise ConversionException(e, sys)

    @staticmethod
    def calculate_exchange_value(
        amount: float,
        exchange_rate: float,
    ) -> float:
        """
        Alias for convert().

        This method provides a more descriptive name for
        future extensibility.

        Args:
            amount: Amount to convert.
            exchange_rate: Exchange rate.

        Returns:
            Converted amount.
        """
        return CurrencyConverter.convert(
            amount=amount,
            exchange_rate=exchange_rate,
        )

    @staticmethod
    def round_currency(
        amount: float,
        decimal_places: int = 2,
    ) -> float:
        """
        Round a currency amount.

        Args:
            amount: Currency amount.
            decimal_places: Number of decimal places.

        Returns:
            Rounded value.
        """
        try:
            rounded_amount = round(amount, decimal_places)

            logging.info(
                "Rounded currency amount to %d decimal places.",
                decimal_places,
            )

            return rounded_amount

        except Exception as e:
            logging.error(
                "Failed to round currency amount: %s",
                str(e),
            )
            raise ConversionException(e, sys)