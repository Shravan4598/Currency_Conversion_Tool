"""
Pipeline module for the AI Currency Converter.

This module orchestrates the complete currency conversion workflow.

Workflow:
    Validate Input
            ↓
    Fetch Exchange Rate
            ↓
    Calculate Converted Amount
            ↓
    Generate AI Explanation
            ↓
    Return Final Response
"""

from __future__ import annotations

import sys
from typing import Any

from src.currency_converter import CurrencyConverter
from src.exception import ConversionException
from src.exchange_api import ExchangeRateService
from src.llm import GeminiService
from src.logger import logging
from src.utils import CurrencyUtils


class CurrencyConversionPipeline:
    """
    Pipeline responsible for coordinating the
    complete currency conversion process.
    """

    def __init__(self) -> None:
        """Initialize application services."""
        self.exchange_service = ExchangeRateService()
        self.currency_converter = CurrencyConverter()
        self.llm_service = GeminiService()

    def run(
        self,
        amount: float,
        source_currency: str,
        target_currency: str,
    ) -> dict[str, Any]:
        """
        Execute the complete currency conversion pipeline.

        Args:
            amount: Amount to convert.
            source_currency: Source currency code.
            target_currency: Target currency code.

        Returns:
            Dictionary containing the conversion result.
        """
        try:
            logging.info("Starting currency conversion pipeline.")

            # ----------------------------------------
            # Validate Inputs
            # ----------------------------------------

            CurrencyUtils.validate_amount(amount)

            source_currency = CurrencyUtils.validate_currency(
                source_currency
            )

            target_currency = CurrencyUtils.validate_currency(
                target_currency
            )

            logging.info("Input validation completed.")

            # ----------------------------------------
            # Fetch Exchange Rate
            # ----------------------------------------

            exchange_rate = self.exchange_service.get_conversion_rate(
                source_currency=source_currency,
                target_currency=target_currency,
            )

            logging.info(
                "Exchange rate fetched successfully."
            )

            # ----------------------------------------
            # Perform Currency Conversion
            # ----------------------------------------

            converted_amount = self.currency_converter.convert(
                amount=amount,
                exchange_rate=exchange_rate,
            )

            logging.info(
                "Currency converted successfully."
            )

            # ----------------------------------------
            # Generate AI Explanation
            # ----------------------------------------

            explanation = (
                self.llm_service.generate_conversion_explanation(
                    amount=amount,
                    source_currency=source_currency,
                    target_currency=target_currency,
                    exchange_rate=exchange_rate,
                    converted_amount=converted_amount,
                )
            )

            logging.info(
                "AI explanation generated successfully."
            )

            # ----------------------------------------
            # Build Response
            # ----------------------------------------

            result = CurrencyUtils.build_conversion_result(
                amount=amount,
                source_currency=source_currency,
                target_currency=target_currency,
                exchange_rate=exchange_rate,
                converted_amount=converted_amount,
                explanation=explanation,
            )

            logging.info(
                "Currency conversion pipeline completed successfully."
            )

            return result

        except Exception as e:
            logging.error(
                "Currency conversion pipeline failed."
            )
            raise ConversionException(e, sys)

    def answer_currency_question(
        self,
        question: str,
    ) -> str:
        """
        Answer a currency-related question using Gemini.

        Args:
            question: User question.

        Returns:
            AI-generated response.
        """
        try:
            logging.info(
                "Processing currency-related question."
            )

            response = self.llm_service.answer_currency_question(
                question
            )

            logging.info(
                "Question answered successfully."
            )

            return response

        except Exception as e:
            logging.error(
                "Failed to answer currency question."
            )
            raise ConversionException(e, sys)