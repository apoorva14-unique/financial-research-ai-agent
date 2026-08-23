# Financial Research & Analytics AI Agent
### Indian Stock Analysis Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Market](https://img.shields.io/badge/Market-NSE%20%7C%20BSE-orange.svg)](https://www.nseindia.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent financial analytics assistant and research tool tailored for the **Indian Equities Market (NSE/BSE)**. The project integrates real-time and historical market data, technical & fundamental indicators, financial news retrieval, sentiment analysis, multi-stock comparison, and an AI agent capable of generating structured equity research reports.

---

## 1. Project Overview

Analyzing Indian equities often requires navigating fragmented data sources for stock prices, technical charts, corporate fundamentals, and news sentiment. The **Financial Research & Analytics AI Agent** unifies these workflows into a single interactive terminal:
- **Indian Market Focus**: Native support for National Stock Exchange (NSE) and Bombay Stock Exchange (BSE) listed equities.
- **Quantitative & Technical Analysis**: Built-in indicators (RSI, MACD, Moving Averages, Bollinger Bands) and fundamental metrics formatted in Indian currency denominations (₹ Lakhs / Crores).
- **Intelligent Assistant**: An AI agent leveraging tool-calling capabilities to answer complex financial queries, compare peer companies, and draft institutional-style equity research reports.

---

## 2. Objectives

- **Automate Market Research**: Streamline historical and real-time data retrieval for Indian equities.
- **Provide Actionable Insights**: Combine quantitative technical indicators with qualitative news sentiment.
- **Enable Peer Comparison**: Offer side-by-side comparative matrices across key valuation ratios and price trends.
- **Facilitate Autonomous AI Analysis**: Equip an LLM with specialized tool calling to execute structured financial research workflows.
- **Promote Transparent Analytics**: Provide citations for data sources and adhere to regulatory compliance disclaimers.

---

## 3. Technology Stack

- **Core & Data Processing**: Python, [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Market Data Feeds**: [yfinance](https://github.com/ranaroussi/yfinance) (with `.NS` and `.BO` ticker resolution)
- **User Interface**: [Streamlit](https://streamlit.io/)
- **Visualizations**: [Plotly](https://plotly.com/python/) (interactive candlestick & indicator charts)
- **Configuration & Environment**: [python-dotenv](https://github.com/theskumar/python-dotenv)
- **Database & Caching**: SQLite
- **AI & Agentic Framework (Planned)**: [LangChain](https://www.langchain.com/) / LangGraph with Tool Calling

---

## 4. Current Implementation

The project is currently in the **Foundation Stage**:
- [x] Project architecture and modular folder hierarchy initialized
- [x] Base dependency management (`requirements.txt`)
- [x] Environment configuration template (`.env.example`)
- [x] Global configuration module (`config/settings.py`)
- [x] Foundation Streamlit entry point (`app.py`)
- [x] SQLite database directory structure (`data/`, `database/`)

---

## 5. Planned Features

1. **Indian Stock Data Retrieval**: Fetch real-time quotes, historical OHLCV data, and corporate profiles for NSE/BSE stocks.
2. **Technical Analysis Engine**: Compute RSI, MACD, Simple & Exponential Moving Averages (20, 50, 200 EMA), Bollinger Bands, and Support/Resistance levels.
3. **Financial News Retrieval**: Ingest news feeds from major Indian financial portals (Moneycontrol, Economic Times, LiveMint).
4. **News Sentiment Analysis**: Score market sentiment (Bullish, Bearish, Neutral) with confidence metrics.
5. **Stock Comparison Module**: Side-by-side comparison of peer stocks on valuation multiples and relative performance.
6. **AI Agent with Tools**: ReAct agent using LangChain tool calling for conversational market research.
7. **SQLite Caching & Persistence**: Cache historical price data, track user watchlists, and store generated research reports.
8. **Streamlit Financial Terminal UI**: Sleek dark-mode interface with interactive charts and step-by-step agent reasoning logs.
9. **AI-Generated Financial Research Reports**: Export structured, institutional-style research notes to Markdown and PDF.
10. **Data Attribution & Disclaimers**: Explicit source citations, timestamps, and mandatory SEBI compliance notices.

---

## 6. How to Run

### Prerequisites
- Python 3.10 or higher
- Git

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/apoorva14-unique/financial-research-ai-agent.git
   cd financial-research-ai-agent
   ```

2. **Create and activate a virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   copy .env.example .env     # On Windows
   # or: cp .env.example .env  # On Linux/macOS
   ```

5. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

---

## 7. Financial Disclaimer

> **IMPORTANT REGULATORY & EDUCATIONAL NOTICE**  
> This software is developed strictly for **educational and research purposes**. It is **not** registered with the Securities and Exchange Board of India (SEBI) or any other regulatory financial authority.  
> 
> The outputs, analytics, and AI-generated content provided by this tool **do not constitute financial advice, investment recommendations, or an endorsement** to buy, sell, or hold any security. Stock markets are subject to market risks. Users should conduct their own independent research or consult a certified financial advisor before making any investment decisions.
