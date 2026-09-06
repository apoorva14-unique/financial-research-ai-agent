"""
Unit tests for analysis/fundamentals.py
Tests fetching fundamental valuation metrics and company ratios.
"""

from analysis.fundamentals import get_fundamentals


def test_get_fundamentals_valid():
    """Test retrieving fundamentals for a valid Indian stock ticker."""
    fundamentals = get_fundamentals("INFY.NS")
    
    assert isinstance(fundamentals, dict)
    
    expected_fields = [
        "company_name",
        "sector",
        "industry",
        "market_cap",
        "pe_ratio",
        "forward_pe",
        "price_to_book",
        "roe",
        "profit_margin",
        "dividend_yield",
    ]
    for field in expected_fields:
        assert field in fundamentals

    assert "Infosys" in fundamentals["company_name"] or "INFY" in fundamentals["company_name"]


def test_get_fundamentals_sector_and_industry():
    """Test that sector and industry are retrieved for a major corporate stock."""
    fundamentals = get_fundamentals("TCS.NS")
    
    assert fundamentals.get("sector") != "N/A"
    assert fundamentals.get("industry") != "N/A"
