import pandas as pd


def calculate_indicators(data):
    """
    Calculate basic technical indicators.
    """

    df = data.copy()

    # Simple Moving Averages
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    # EMA
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()

    # RSI
    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    # Bollinger Bands
    middle = df["Close"].rolling(window=20).mean()
    std = df["Close"].rolling(window=20).std()

    df["BB_Upper"] = middle + (2 * std)
    df["BB_Lower"] = middle - (2 * std)

    return df


def get_latest_indicators(data):
    """
    Return the latest technical indicator values.
    """

    df = calculate_indicators(data)

    latest = df.iloc[-1]

    return {
        "close": float(latest["Close"]),
        "sma_20": float(latest["SMA_20"]),
        "sma_50": float(latest["SMA_50"]),
        "ema_20": float(latest["EMA_20"]),
        "rsi": float(latest["RSI"]),
        "macd": float(latest["MACD"]),
        "macd_signal": float(latest["MACD_Signal"]),
    }