from data.stock_data import get_stock_history, get_stock_info
from analysis.technical import get_latest_indicators
from analysis.fundamentals import get_fundamentals
from data.news_data import get_stock_news


def _normalize_ticker(ticker: str) -> str:
    """Helper to ensure Indian stock tickers have proper exchange suffix (.NS default)."""
    if not ticker or not isinstance(ticker, str):
        return ""
    clean = ticker.strip().upper()
    # If no exchange suffix is provided, default to NSE (.NS)
    if "." not in clean and ":" not in clean:
        clean = f"{clean}.NS"
    return clean


def stock_price_tool(ticker):
    """Fetch current price, high, low, and volume for a ticker."""
    try:
        norm_ticker = _normalize_ticker(ticker)
        data = get_stock_history(norm_ticker, period="1mo")

        if data.empty:
            return {"error": f"No price data available for ticker '{ticker}'."}

        latest = data.iloc[-1]

        return {
            "ticker": norm_ticker,
            "price": round(float(latest["Close"]), 2),
            "high": round(float(latest["High"]), 2),
            "low": round(float(latest["Low"]), 2),
            "volume": int(latest["Volume"])
        }
    except Exception as e:
        return {"error": f"Failed to fetch stock price for '{ticker}': {str(e)}"}


def technical_analysis_tool(ticker):
    """Fetch RSI, SMA 20/50, EMA, and MACD indicators for a ticker."""
    try:
        norm_ticker = _normalize_ticker(ticker)
        data = get_stock_history(norm_ticker, period="1y")

        if data.empty or len(data) < 20:
            return {"error": f"Insufficient historical data to compute technicals for '{ticker}'."}

        return get_latest_indicators(data)
    except Exception as e:
        return {"error": f"Failed to compute technical analysis for '{ticker}': {str(e)}"}


def fundamentals_tool(ticker):
    """Fetch fundamental valuation ratios and company info."""
    try:
        norm_ticker = _normalize_ticker(ticker)
        return get_fundamentals(norm_ticker)
    except Exception as e:
        return {"error": f"Failed to fetch fundamentals for '{ticker}': {str(e)}"}


def news_tool(company_name):
    """Fetch recent news articles for a company."""
    try:
        if not company_name:
            return {"error": "Company name is required for news lookup."}
        articles = get_stock_news(company_name)
        if not articles:
            return {"message": f"No recent news found for '{company_name}'."}
        return articles
    except Exception as e:
        return {"error": f"Failed to fetch news for '{company_name}': {str(e)}"}