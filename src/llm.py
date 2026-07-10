"""
LLM service module for the AI Currency Converter.

This module handles all interactions with the Google Gemini model
to generate natural language explanations for currency conversions.
"""

from __future__ import annotations

import sys

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.config import config
from src.exception import ConversionException
from src.logger import logging
from src.prompt import CurrencyPrompt


class GeminiService:
    """
    Service class responsible for interacting with the Gemini LLM.
    """

    def __init__(self) -> None:
        """
        Initialize the Gemini language model.
        """
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=config.model.model_name,
                google_api_key=config.env.google_api_key,
                temperature=config.model.temperature,
            )

            self.output_parser = StrOutputParser()

            logging.info("Gemini model initialized successfully.")

        except Exception as e:
            logging.error("Failed to initialize Gemini model.")
            raise ConversionException(e, sys)

    def generate_conversion_explanation(
        self,
        amount: float,
        source_currency: str,
        target_currency: str,
        exchange_rate: float,
        converted_amount: float,
    ) -> str:
        """
        Generate a natural language explanation for a currency conversion.

        Args:
            amount: Original amount.
            source_currency: Source currency.
            target_currency: Target currency.
            exchange_rate: Exchange rate.
            converted_amount: Converted amount.

        Returns:
            Natural language explanation.
        """
        try:
            prompt = PromptTemplate(
                template=CurrencyPrompt.CONVERSION_EXPLANATION,
                input_variables=[
                    "amount",
                    "source_currency",
                    "target_currency",
                    "exchange_rate",
                    "converted_amount",
                ],
            )

            chain = prompt | self.llm | self.output_parser

            explanation = chain.invoke(
                {
                    "amount": amount,
                    "source_currency": source_currency,
                    "target_currency": target_currency,
                    "exchange_rate": exchange_rate,
                    "converted_amount": converted_amount,
                }
            )

            logging.info("Conversion explanation generated successfully.")

            return explanation.strip()

        except Exception as e:
            logging.error("Failed to generate conversion explanation.")
            raise ConversionException(e, sys)

    def answer_currency_question(
        self,
        question: str,
    ) -> str:
        """
        Answer a currency-related question.

        Args:
            question: User question.

        Returns:
            AI-generated answer.
        """
        try:
            prompt = PromptTemplate(
                template=CurrencyPrompt.GENERAL_QA,
                input_variables=["question"],
            )

            chain = prompt | self.llm | self.output_parser

            response = chain.invoke(
                {
                    "question": question
                }
            )

            logging.info("Currency question answered successfully.")

            return response.strip()

        except Exception as e:
            logging.error("Failed to answer currency question.")
            raise ConversionException(e, sys)

    def explain_error(
        self,
        error_message: str,
    ) -> str:
        """
        Generate a user-friendly explanation for an error.

        Args:
            error_message: Technical error.

        Returns:
            Friendly explanation.
        """
        try:
            prompt = PromptTemplate(
                template=CurrencyPrompt.ERROR_EXPLANATION,
                input_variables=["error"],
            )

            chain = prompt | self.llm | self.output_parser

            response = chain.invoke(
                {
                    "error": error_message
                }
            )

            logging.info("Error explanation generated successfully.")

            return response.strip()

        except Exception:
            logging.exception("Unable to generate AI error explanation.")
            return (
                "Something went wrong while processing your request. "
                "Please try again later."
            )