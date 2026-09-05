import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote


def get_stock_news(company_name, limit=5):
    """
    Fetch recent financial news using Google News RSS.
    """

    query = quote(f"{company_name} stock India")

    url = (
        f"https://news.google.com/rss/search?"
        f"q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    articles = []

    for item in root.findall(".//item")[:limit]:

        title = item.findtext("title")
        link = item.findtext("link")
        pub_date = item.findtext("pubDate")

        articles.append({
            "title": title,
            "link": link,
            "published": pub_date
        })

    return articles