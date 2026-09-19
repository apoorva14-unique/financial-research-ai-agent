"""
Sentiment Analysis Engine for Financial News Headlines.

Uses the VADER (Valence Aware Dictionary and sEntiment Reasoner) rule-based
sentiment analysis tool to assess financial news headlines.

IMPORTANT COMPLIANCE & USAGE NOTICE:
This module performs basic rule-based lexical sentiment scoring. It is designed
strictly for educational and research purposes and DOES NOT constitute professional
financial or investment advice. Rule-based sentiment analysis does not predict stock
market returns or evaluate real-world economic fundamentals.
"""

import logging
from typing import Any, Dict, List, Optional

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    # Fallback to nltk if vaderSentiment is unavailable
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

# Initialize analyzer instance once for reuse across calls
_analyzer: Optional[SentimentIntensityAnalyzer] = None


def get_sentiment_analyzer() -> SentimentIntensityAnalyzer:
    """Return a singleton instance of SentimentIntensityAnalyzer."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def classify_compound_score(score: float) -> str:
    """
    Classify a VADER compound score into Track A sentiment categories:
    - Positive: score >= 0.5
    - Negative: score <= -0.5
    - Neutral:  -0.5 < score < 0.5
    """
    if score >= 0.5:
        return "Positive"
    elif score <= -0.5:
        return "Negative"
    else:
        return "Neutral"


def analyze_headline_sentiment(headline: Optional[str]) -> Dict[str, Any]:
    """
    Analyze the sentiment of a single financial news headline using VADER.

    Safely handles None, non-string, and empty or whitespace-only inputs by
    defaulting to a neutral score (0.0).

    Returns:
        dict: {
            "sentiment_score": float (rounded compound score between -1.0 and 1.0),
            "sentiment_label": "Positive" | "Negative" | "Neutral"
        }
    """
    if headline is None or not isinstance(headline, str):
        return {
            "sentiment_score": 0.0,
            "sentiment_label": "Neutral",
        }

    clean_text = headline.strip()
    if not clean_text:
        return {
            "sentiment_score": 0.0,
            "sentiment_label": "Neutral",
        }

    try:
        analyzer = get_sentiment_analyzer()
        scores = analyzer.polarity_scores(clean_text)
        compound = round(float(scores.get("compound", 0.0)), 4)
        label = classify_compound_score(compound)

        return {
            "sentiment_score": compound,
            "sentiment_label": label,
        }
    except Exception as e:
        logger.warning(f"Failed to analyze sentiment for headline '{clean_text[:50]}...': {e}")
        return {
            "sentiment_score": 0.0,
            "sentiment_label": "Neutral",
        }


def analyze_news_sentiment(articles: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Enrich a list of news article dictionaries with sentiment analysis fields:
    - 'sentiment_score': float
    - 'sentiment_label': 'Positive' | 'Negative' | 'Neutral'

    Guarantees that an error on any individual article does not crash
    the entire application.
    """
    if not articles or not isinstance(articles, list):
        return []

    enriched_articles = []
    for article in articles:
        if not isinstance(article, dict):
            continue

        item = dict(article)
        headline = item.get("title")

        try:
            sentiment_result = analyze_headline_sentiment(headline)
            item["sentiment_score"] = sentiment_result["sentiment_score"]
            item["sentiment_label"] = sentiment_result["sentiment_label"]
        except Exception as err:
            logger.error(f"Error analyzing article '{headline}': {err}")
            item["sentiment_score"] = 0.0
            item["sentiment_label"] = "Neutral"

        enriched_articles.append(item)

    return enriched_articles


def calculate_sentiment_summary(articles: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Calculate summary statistics across an article list:
    - total_articles: Total count of processed articles
    - positive_count: Count of Positive articles (compound >= 0.5)
    - negative_count: Count of Negative articles (compound <= -0.5)
    - neutral_count:  Count of Neutral articles (-0.5 < compound < 0.5)
    - average_sentiment_score: Mean compound score across all articles
    - overall_sentiment: Overall category based on the average score
    """
    if not articles or not isinstance(articles, list):
        return {
            "total_articles": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "average_sentiment_score": 0.0,
            "overall_sentiment": "Neutral",
        }

    total = len(articles)
    positive = 0
    negative = 0
    neutral = 0
    score_sum = 0.0

    for a in articles:
        score = a.get("sentiment_score", 0.0)
        label = a.get("sentiment_label") or classify_compound_score(score)

        if label == "Positive":
            positive += 1
        elif label == "Negative":
            negative += 1
        else:
            neutral += 1

        score_sum += float(score)

    avg_score = round(score_sum / total, 4) if total > 0 else 0.0
    overall = classify_compound_score(avg_score)

    return {
        "total_articles": total,
        "positive_count": positive,
        "negative_count": negative,
        "neutral_count": neutral,
        "average_sentiment_score": avg_score,
        "overall_sentiment": overall,
    }
