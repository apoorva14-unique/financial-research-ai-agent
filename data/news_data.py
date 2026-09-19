"""
Financial News Data Retrieval Module.

Fetches recent Indian equity market news via Google News RSS, extracts publication
metadata (title, link, date, source), and enriches articles with VADER sentiment scores.
"""

import logging
import xml.etree.ElementTree as ET
from urllib.parse import quote
from typing import Any, Dict, List, Optional

import requests

from analysis.sentiment import analyze_news_sentiment

logger = logging.getLogger(__name__)


def extract_source_from_item(item: ET.Element, title: Optional[str] = None) -> str:
    """Extract publication source name from XML source element or title suffix."""
    source_elem = item.find("source")
    if source_elem is not None and source_elem.text and source_elem.text.strip():
        return source_elem.text.strip()

    # Fallback: Google News RSS titles frequently end in ' - Source Name'
    if title and " - " in title:
        parts = title.rsplit(" - ", 1)
        if len(parts) == 2 and parts[1].strip():
            return parts[1].strip()

    return "Unknown Source"


def get_stock_news(company_name: Optional[str], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch recent financial news using Google News RSS and enrich with sentiment analysis.

    Args:
        company_name: Name of the company or equity ticker (e.g. 'Reliance', 'TCS').
        limit: Maximum number of news articles to retrieve (default 5).

    Returns:
        List of dicts containing:
        - title: Article headline
        - link: URL to the article
        - published: Publication timestamp
        - source: Publishing media house
        - sentiment_score: VADER compound score
        - sentiment_label: 'Positive' | 'Negative' | 'Neutral'
    """
    if not company_name or not isinstance(company_name, str) or not company_name.strip():
        logger.warning("Empty or invalid company name provided to get_stock_news.")
        return []

    clean_name = company_name.strip()
    query = quote(f"{clean_name} stock India")

    url = (
        f"https://news.google.com/rss/search?"
        f"q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error(f"Network timeout while fetching news for '{clean_name}'.")
        return []
    except requests.exceptions.RequestException as req_err:
        logger.error(f"HTTP request error fetching news for '{clean_name}': {req_err}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error requesting news for '{clean_name}': {e}")
        return []

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as parse_err:
        logger.error(f"Failed to parse RSS XML for '{clean_name}': {parse_err}")
        return []

    raw_articles = []
    items = root.findall(".//item")

    for item in items[:limit]:
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        pub_date = item.findtext("pubDate") or "Date unavailable"
        source = extract_source_from_item(item, title)

        raw_articles.append({
            "title": title.strip(),
            "link": link.strip(),
            "published": pub_date.strip(),
            "source": source
        })

    # Enrich raw articles with sentiment analysis (VADER)
    enriched_articles = analyze_news_sentiment(raw_articles)
    return enriched_articles