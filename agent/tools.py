from data.stock_data import get_stock_history, get_stock_info
from analysis.technical import get_latest_indicators
from analysis.fundamentals import get_fundamentals
from data.news_data import get_stock_news


def stock_price_tool(ticker):
    data = get_stock_history(ticker, period="1mo")

    latest = data.iloc[-1]

    return {
        "ticker": ticker,
        "price": float(latest["Close"]),
        "high": float(latest["High"]),
        "low": float(latest["Low"]),
        "volume": int(latest["Volume"])
    }


def technical_analysis_tool(ticker):
    data = get_stock_history(ticker, period="1y")

    return get_latest_indicators(data)


def fundamentals_tool(ticker):
    return get_fundamentals(ticker)


def news_tool(company_name):
    return get_stock_news(company_name)