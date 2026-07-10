"""
Streamlit application for the AI Currency Converter.
"""

from __future__ import annotations

import streamlit as st

from src.config import config
from src.pipeline import CurrencyConversionPipeline


st.set_page_config(
    page_title=config.app.app_title,
    page_icon=config.app.app_icon,
    layout=config.app.page_layout,
)

pipeline = CurrencyConversionPipeline()

st.sidebar.title("💱 AI Currency Converter")
st.sidebar.info(
    """
Convert currencies using real-time exchange rates
powered by the Exchange Rate API.

Receive an AI-generated explanation
using Google Gemini.
"""
)

st.title(config.app.app_title)

st.write(
    "Convert currencies using real-time exchange rates and get an AI-generated explanation."
)

currencies = config.app.supported_currencies

col1, col2 = st.columns(2)

with col1:
    source_currency = st.selectbox(
        "Source Currency",
        currencies,
        index=currencies.index(config.app.default_source_currency),
    )

with col2:
    target_currency = st.selectbox(
        "Target Currency",
        currencies,
        index=currencies.index(config.app.default_target_currency),
    )

amount = st.number_input(
    "Amount",
    min_value=0.01,
    value=100.0,
    step=1.0,
)

if st.button("Convert", use_container_width=True):

    with st.spinner("Fetching latest exchange rates..."):

        try:
            result = pipeline.run(
                amount=amount,
                source_currency=source_currency,
                target_currency=target_currency,
            )

            st.success("Conversion Successful")

            st.metric(
                "Converted Amount",
                result["formatted_result"],
            )

            st.metric(
                "Exchange Rate",
                f"1 {source_currency} = {result['exchange_rate']:.6f} {target_currency}",
            )

            with st.expander(
                "AI Explanation",
                expanded=True,
            ):
                st.write(result["explanation"])

        except Exception as e:
            st.error(str(e))