import os

import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

from data.stock_data import get_stock_history, get_stock_info
from analysis.technical import calculate_indicators
from analysis.fundamentals import get_fundamentals
from data.news_data import get_stock_news
from ui.chat import render_agent_chat


load_dotenv()

st.set_page_config(
    page_title="Financial Research AI Agent",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Financial Research & Analytics AI Agent")

st.caption(
    "Indian Equity Research Assistant for NSE/BSE Stocks"
)


# -------------------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------------------

st.sidebar.header("Stock Selection")

ticker = st.sidebar.text_input(
    "Enter NSE ticker",
    "RELIANCE.NS"
).upper()


period = st.sidebar.selectbox(
    "Historical Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)

# Manage dashboard analysis state across Streamlit reruns
if st.sidebar.button("Analyze Stock"):
    st.session_state["analyzed_ticker"] = ticker
    st.session_state["analyzed_period"] = period


import math
import pandas as pd

# -------------------------------------------------------------
# DISPLAY FORMATTING HELPERS (GRACEFUL HANDLING OF NONE / NAN)
# -------------------------------------------------------------

def format_number(val, decimals=2) -> str:
    """Format a numerical value to fixed decimal places; returns 'N/A' for None/NaN/inf."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return "N/A"
        return f"{f:,.{decimals}f}"
    except (ValueError, TypeError):
        return "N/A"


def format_currency(val, symbol="₹", decimals=2) -> str:
    """Format a price or currency value; returns 'N/A' for None/NaN/inf."""
    formatted = format_number(val, decimals=decimals)
    if formatted == "N/A":
        return "N/A"
    return f"{symbol}{formatted}"


def format_percent(val, decimals=2) -> str:
    """Format a ratio/decimal as a percentage; returns 'N/A' for None/NaN/inf."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return "N/A"
        return f"{f * 100:.{decimals}f}%"
    except (ValueError, TypeError):
        return "N/A"


def format_text(val) -> str:
    """Clean text display; returns 'N/A' for missing or empty text."""
    if val is None or pd.isna(val):
        return "N/A"
    s = str(val).strip()
    if not s or s.lower() in ("none", "nan", "null"):
        return "N/A"
    return s


# -------------------------------------------------------------
# 1. STOCK ANALYSIS DASHBOARD (CHARTS & INDICATORS)
# -------------------------------------------------------------

active_ticker = st.session_state.get("analyzed_ticker")
active_period = st.session_state.get("analyzed_period", period)

if active_ticker:
    with st.spinner("Fetching financial data..."):
        try:
            data = get_stock_history(
                active_ticker,
                period=active_period
            )

            data = data.dropna(
                subset=["Open", "High", "Low", "Close"]
            )

            info = get_stock_info(active_ticker)
            fundamentals = get_fundamentals(active_ticker)
            technical = calculate_indicators(data)

            company_name = info.get(
                "longName",
                active_ticker
            )

            st.success(
                f"Analysis loaded for {company_name}"
            )

            # -----------------------
            # PRICE INFORMATION
            # -----------------------
            latest_price = data["Close"].iloc[-1] if not data.empty else None
            previous_price = data["Close"].iloc[-2] if len(data) > 1 else None

            if latest_price is not None and previous_price is not None:
                change = latest_price - previous_price
                change_percent = (change / previous_price) * 100 if previous_price != 0 else None
            else:
                change = None
                change_percent = None

            vol_val = data["Volume"].iloc[-1] if not data.empty else None
            vol_str = f"{int(vol_val):,}" if (vol_val is not None and not pd.isna(vol_val)) else "N/A"

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Current Price",
                format_currency(latest_price)
            )

            col2.metric(
                "Daily Change",
                format_currency(change),
                f"{change_percent:+.2f}%" if (change_percent is not None and not pd.isna(change_percent)) else "N/A"
            )

            col3.metric(
                "Volume",
                vol_str
            )

            # -----------------------
            # PRICE CHART
            # -----------------------
            st.subheader("Price Chart")

            fig = go.Figure()

            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data["Open"],
                    high=data["High"],
                    low=data["Low"],
                    close=data["Close"],
                    name="Price"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=technical["SMA_20"],
                    name="SMA 20"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=technical["SMA_50"],
                    name="SMA 50"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # -----------------------
            # TECHNICAL INDICATORS
            # -----------------------
            st.subheader("Technical Analysis")

            latest = technical.iloc[-1] if not technical.empty else {}

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "RSI",
                format_number(latest.get("RSI"))
            )

            col2.metric(
                "SMA 20",
                format_currency(latest.get("SMA_20"))
            )

            col3.metric(
                "SMA 50",
                format_currency(latest.get("SMA_50"))
            )

            col4.metric(
                "MACD",
                format_number(latest.get("MACD"))
            )

            # -----------------------
            # FUNDAMENTALS
            # -----------------------
            st.subheader("Fundamental Analysis")

            f1, f2, f3, f4 = st.columns(4)

            f1.metric(
                "P/E Ratio",
                format_number(fundamentals.get("pe_ratio"))
            )

            f2.metric(
                "P/B Ratio",
                format_number(fundamentals.get("price_to_book"))
            )

            f3.metric(
                "ROE",
                format_percent(fundamentals.get("roe"))
            )

            f4.metric(
                "Profit Margin",
                format_percent(fundamentals.get("profit_margin"))
            )

            st.write(
                "Sector:",
                format_text(fundamentals.get("sector"))
            )

            st.write(
                "Industry:",
                format_text(fundamentals.get("industry"))
            )

            # -----------------------
            # NEWS
            # -----------------------
            st.subheader("Latest Financial News")

            news = get_stock_news(
                fundamentals.get("company_name", active_ticker)
            )

            for article in news:
                st.markdown(
                    f"**{article['title']}**"
                )

                st.caption(
                    article["published"]
                )

                st.markdown(
                    article["link"]
                )

        except Exception as e:
            st.error(
                f"Unable to analyze {active_ticker}: {e}"
            )
else:
    st.info("👈 Enter an NSE ticker (e.g. `RELIANCE.NS`, `TCS.NS`, `INFY.NS`) in the sidebar and click **Analyze Stock** to view candlestick charts, technical indicators, and fundamental metrics.")


# -------------------------------------------------------------
# 2. AI RESEARCH ASSISTANT (CHAT INTERFACE)
# -------------------------------------------------------------
st.divider()
render_agent_chat(show_disclaimer=False)


# -------------------------------------------------------------
# 3. DISCLAIMER
# -------------------------------------------------------------
st.divider()

st.warning(
    "Educational & Research Purpose Only. "
    "This tool is not a SEBI registered investment advisor. "
    "The information and AI-generated analysis presented "
    "do not constitute financial advice or a recommendation "
    "to buy or sell securities."
)