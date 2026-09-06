"""
Unit tests for analysis/technical.py
Tests calculation of moving averages, RSI, and MACD indicators.
"""

import numpy as np
import pandas as pd
from analysis.technical import calculate_indicators, get_latest_indicators


def create_sample_price_data(days=60):
    """Helper to generate sample price data for indicator calculation."""
    dates = pd.date_range(start="2026-01-01", periods=days, freq="B")
    # Simulated upward-drifting price series
    prices = 1000.0 + np.cumsum(np.linspace(0.5, 2.0, days))
    
    return pd.DataFrame({
        "Open": prices - 2.0,
        "High": prices + 5.0,
        "Low": prices - 5.0,
        "Close": prices,
        "Volume": 1000000
    }, index=dates)


def test_calculate_indicators():
    """Test that all required technical indicators are added to DataFrame."""
    df = create_sample_price_data(days=60)
    result_df = calculate_indicators(df)
    
    expected_indicators = [
        "SMA_20", "SMA_50", "EMA_20", "RSI", "MACD", "MACD_Signal", "BB_Upper", "BB_Lower"
    ]
    for ind in expected_indicators:
        assert ind in result_df.columns

    # Verify latest RSI is within standard bound [0, 100]
    latest_rsi = result_df["RSI"].iloc[-1]
    assert 0 <= latest_rsi <= 100


def test_get_latest_indicators():
    """Test extracting the latest indicator metrics dictionary."""
    df = create_sample_price_data(days=60)
    latest = get_latest_indicators(df)
    
    assert isinstance(latest, dict)
    expected_keys = ["close", "sma_20", "sma_50", "ema_20", "rsi", "macd", "macd_signal"]
    for key in expected_keys:
        assert key in latest
        assert isinstance(latest[key], float)
