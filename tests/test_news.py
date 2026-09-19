"""
Unit tests for data/news_data.py
Tests fetching recent financial news via Google News RSS, error handling,
source parsing, and sentiment enrichment.
"""

from unittest.mock import MagicMock, patch
import requests
from data.news_data import get_stock_news


def test_get_stock_news_returns_articles_with_sentiment():
    """Test fetching recent financial news articles and verifying sentiment fields."""
    articles = get_stock_news("Reliance", limit=3)

    assert isinstance(articles, list)
    if articles:
        assert len(articles) <= 3
        first = articles[0]
        assert "title" in first
        assert "link" in first
        assert "published" in first
        assert "source" in first
        assert "sentiment_score" in first
        assert "sentiment_label" in first
        assert first["sentiment_label"] in ["Positive", "Negative", "Neutral"]
        assert isinstance(first["sentiment_score"], float)


def test_get_stock_news_respects_limit():
    """Test that the limit parameter restricts the number of returned articles."""
    articles = get_stock_news("Tata Motors", limit=2)
    assert len(articles) <= 2


def test_get_stock_news_invalid_company_name():
    """Test that invalid or empty company names return an empty list gracefully."""
    assert get_stock_news("") == []
    assert get_stock_news("   ") == []
    assert get_stock_news(None) == []


@patch("data.news_data.requests.get")
def test_get_stock_news_network_timeout(mock_get):
    """Test that network timeouts are handled safely without raising an exception."""
    mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")
    articles = get_stock_news("Infosys")
    assert articles == []


@patch("data.news_data.requests.get")
def test_get_stock_news_http_error(mock_get):
    """Test that HTTP request errors return an empty list safely."""
    mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")
    articles = get_stock_news("Wipro")
    assert articles == []


@patch("data.news_data.requests.get")
def test_get_stock_news_malformed_xml(mock_get):
    """Test that malformed XML returns an empty list without crashing."""
    mock_response = MagicMock()
    mock_response.content = b"<<<not-valid-xml>>>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    articles = get_stock_news("HDFC")
    assert articles == []


@patch("data.news_data.requests.get")
def test_get_stock_news_mocked_success(mock_get):
    """Test parsing of mocked RSS items including source and sentiment tags."""
    sample_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <item>
          <title>Record quarterly profits boost corporate outlook - Mint</title>
          <link>https://example.com/item1</link>
          <pubDate>Sat, 19 Sep 2026 10:00:00 GMT</pubDate>
          <source url="https://livemint.com">Mint</source>
        </item>
      </channel>
    </rss>"""

    mock_response = MagicMock()
    mock_response.content = sample_xml
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    articles = get_stock_news("Sample Corp", limit=1)
    assert len(articles) == 1
    assert articles[0]["title"] == "Record quarterly profits boost corporate outlook - Mint"
    assert articles[0]["source"] == "Mint"
    assert "sentiment_score" in articles[0]
    assert "sentiment_label" in articles[0]
    assert articles[0]["sentiment_label"] in ["Positive", "Neutral"]
