"""
Unit tests for data/stock_data.py
Tests fetching historical stock data and basic stock information.
"""

import pandas as pd
import pytest
from data.stock_data import get_stock_history, get_stock_info


def test_get_stock_history_valid():
    """Test fetching historical OHLCV data for a valid ticker."""
    df = get_stock_history("RELIANCE.NS", period="5d")
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        assert col in df.columns


def test_get_stock_history_invalid():
    """Test that fetching data for a non-existent ticker raises RuntimeError."""
    with pytest.raises(RuntimeError):
        get_stock_history("INVALID_TICKER_XYZ_999", period="5d")


def test_get_stock_info_valid():
    """Test fetching basic company information for a valid ticker."""
    info = get_stock_info("TCS.NS")
    
    assert isinstance(info, dict)
    assert len(info) > 0
    assert "symbol" in info or "shortName" in info or "longName" in info
