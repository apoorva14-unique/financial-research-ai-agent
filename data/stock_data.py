import yfinance as yf


def get_stock_history(ticker, period="1y"):
    """
    Fetch historical OHLCV data for a stock.
    """

    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)

        if data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")

        return data

    except Exception as e:
        raise RuntimeError(
            f"Failed to fetch stock data for {ticker}: {e}"
        )


def get_stock_info(ticker):
    """
    Fetch basic information about a stock.
    """

    try:
        stock = yf.Ticker(ticker)
        return stock.info

    except Exception as e:
        raise RuntimeError(
            f"Failed to fetch stock information for {ticker}: {e}"
        )