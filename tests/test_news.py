"""
Unit tests for data/news_data.py
Tests fetching recent financial news via Google News RSS.
"""

from data.news_data import get_stock_news


def test_get_stock_news_returns_articles():
    """Test fetching recent financial news articles for a company."""
    articles = get_stock_news("Reliance", limit=3)
    
    assert isinstance(articles, list)
    assert len(articles) > 0
    assert len(articles) <= 3
    
    first = articles[0]
    assert "title" in first
    assert "link" in first
    assert "published" in first
    assert first["link"].startswith("http")


def test_get_stock_news_respects_limit():
    """Test that the limit parameter restricts the number of returned articles."""
    articles = get_stock_news("Tata Motors", limit=2)
    assert len(articles) <= 2
