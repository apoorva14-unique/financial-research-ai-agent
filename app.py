"""
Financial Research & Analytics AI Agent - Streamlit Application Entrance.
Foundation Stage.
"""

import streamlit as st
from config.settings import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    APP_LAYOUT,
    DEFAULT_TICKERS,
    SEBI_DISCLAIMER,
)

# Configure Streamlit page settings
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded",
)

# Header Section
st.title(f"{APP_ICON} {APP_TITLE}")
st.caption(f"**{APP_SUBTITLE}** | Phase 1: Foundation & Architecture Setup")

st.markdown("---")

# Main Content Card / Status
st.subheader("📌 Project Status: Foundation Initialized")
st.info(
    "Welcome to the **Financial Research & Analytics AI Agent** workspace. "
    "The environment and project skeleton are now established. "
    "Subsequent modules will be implemented incrementally across the development roadmap."
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Core Capabilities (Planned Roadmap)")
    st.markdown(
        """
        - 📊 **Indian Stock Data Retrieval**: Live & historical data from NSE/BSE.
        - 📈 **Technical Analysis**: Real-time indicators (RSI, MACD, EMAs, Bollinger Bands).
        - 🏢 **Fundamental Valuation**: P/E, P/B, ROE, Debt/Equity in Indian Denominations (₹ Cr).
        - 📰 **Financial News & Sentiment**: Real-time Indian market news with sentiment analysis.
        - ⚔️ **Stock Comparison**: Peer comparison across technicals, fundamentals, and returns.
        - 🤖 **AI Research Agent**: LangChain/ReAct autonomous financial research workflows.
        - 📑 **Research Reports**: Downloadable institutional-grade PDF and Markdown reports.
        """
    )

with col2:
    st.markdown("### ⚙️ Quick Reference")
    st.markdown("**Sample Tracked Indian Tickers:**")
    st.code("\n".join(DEFAULT_TICKERS), language="text")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.write("**Environment:** Development")
    st.write("**Target Markets:** NSE & BSE")
    st.markdown("---")
    st.caption("v0.1.0 • Foundation Release")

# Financial Disclaimer Footer
st.markdown("---")
st.warning(f"⚖️ **Regulatory Disclaimer:**\n\n{SEBI_DISCLAIMER}")
