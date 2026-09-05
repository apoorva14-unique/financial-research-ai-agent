import os

import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

from data.stock_data import get_stock_history, get_stock_info
from analysis.technical import calculate_indicators
from analysis.fundamentals import get_fundamentals
from data.news_data import get_stock_news


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


st.sidebar.header("Stock Selection")

ticker = st.sidebar.text_input(
    "Enter NSE ticker",
    "RELIANCE.NS"
).upper()


period = st.sidebar.selectbox(
    "Historical Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)


if st.sidebar.button("Analyze Stock"):

    with st.spinner("Fetching financial data..."):

        try:

            data = get_stock_history(
                ticker,
                period=period
            )

            data = data.dropna(
                subset=["Open", "High", "Low", "Close"]
            )

            info = get_stock_info(ticker)

            fundamentals = get_fundamentals(ticker)

            technical = calculate_indicators(data)

            company_name = info.get(
                "longName",
                ticker
            )

            st.success(
                f"Analysis loaded for {company_name}"
            )


            # -----------------------
            # PRICE INFORMATION
            # -----------------------

            latest_price = float(
                data["Close"].iloc[-1]
            )

            previous_price = float(
                data["Close"].iloc[-2]
            )

            change = latest_price - previous_price

            change_percent = (
                change / previous_price
            ) * 100


            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Current Price",
                f"₹{latest_price:,.2f}"
            )

            col2.metric(
                "Daily Change",
                f"₹{change:,.2f}",
                f"{change_percent:.2f}%"
            )

            col3.metric(
                "Volume",
                f"{int(data['Volume'].iloc[-1]):,}"
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

            latest = technical.iloc[-1]

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "RSI",
                f"{latest['RSI']:.2f}"
            )

            col2.metric(
                "SMA 20",
                f"₹{latest['SMA_20']:.2f}"
            )

            col3.metric(
                "SMA 50",
                f"₹{latest['SMA_50']:.2f}"
            )

            col4.metric(
                "MACD",
                f"{latest['MACD']:.2f}"
            )


            # -----------------------
            # FUNDAMENTALS
            # -----------------------

            st.subheader("Fundamental Analysis")

            f1, f2, f3, f4 = st.columns(4)

            f1.metric(
                "P/E Ratio",
                str(fundamentals["pe_ratio"])
            )

            f2.metric(
                "P/B Ratio",
                str(fundamentals["price_to_book"])
            )

            f3.metric(
                "ROE",
                str(fundamentals["roe"])
            )

            f4.metric(
                "Profit Margin",
                str(fundamentals["profit_margin"])
            )


            st.write(
                "Sector:",
                fundamentals["sector"]
            )

            st.write(
                "Industry:",
                fundamentals["industry"]
            )


            # -----------------------
            # NEWS
            # -----------------------

            st.subheader("Latest Financial News")

            news = get_stock_news(
                fundamentals["company_name"]
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
                f"Unable to analyze {ticker}: {e}"
            )


# -----------------------
# DISCLAIMER
# -----------------------

st.divider()

st.warning(
    "Educational & Research Purpose Only. "
    "This tool is not a SEBI registered investment advisor. "
    "The information and AI-generated analysis presented "
    "do not constitute financial advice or a recommendation "
    "to buy or sell securities."
)