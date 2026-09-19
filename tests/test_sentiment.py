"""
Unit tests for analysis/sentiment.py.
Covers VADER sentiment classification, compound score thresholds, edge cases,
and summary calculations without live API dependency.
"""

import pytest
from analysis.sentiment import (
    analyze_headline_sentiment,
    analyze_news_sentiment,
    calculate_sentiment_summary,
    classify_compound_score,
)


def test_positive_headline_sentiment():
    """Test that a strongly optimistic headline is classified as Positive (score >= 0.5)."""
    headline = "Reliance quarterly profit jumps 35% to record high with exceptional dividend growth"
    result = analyze_headline_sentiment(headline)

    assert isinstance(result, dict)
    assert "sentiment_score" in result
    assert "sentiment_label" in result
    assert result["sentiment_score"] >= 0.5
    assert result["sentiment_label"] == "Positive"


def test_negative_headline_sentiment():
    """Test that a strongly pessimistic headline is classified as Negative (score <= -0.5)."""
    headline = "Tata Motors reports disastrous loss and severe sales crash amid deep crisis"
    result = analyze_headline_sentiment(headline)

    assert isinstance(result, dict)
    assert "sentiment_score" in result
    assert "sentiment_label" in result
    assert result["sentiment_score"] <= -0.5
    assert result["sentiment_label"] == "Negative"


def test_neutral_headline_sentiment():
    """Test that a factual or balanced headline is classified as Neutral (-0.5 < score < 0.5)."""
    headline = "Infosys board to meet on October 15 to consider quarterly financial results"
    result = analyze_headline_sentiment(headline)

    assert isinstance(result, dict)
    assert "sentiment_score" in result
    assert "sentiment_label" in result
    assert -0.5 < result["sentiment_score"] < 0.5
    assert result["sentiment_label"] == "Neutral"


def test_empty_headline_handling():
    """Test that empty string or whitespace-only headlines return Neutral score safely."""
    res_empty = analyze_headline_sentiment("")
    assert res_empty["sentiment_score"] == 0.0
    assert res_empty["sentiment_label"] == "Neutral"

    res_whitespace = analyze_headline_sentiment("    \n\t  ")
    assert res_whitespace["sentiment_score"] == 0.0
    assert res_whitespace["sentiment_label"] == "Neutral"


def test_missing_headline_handling():
    """Test that None or non-string inputs do not raise exceptions and return Neutral."""
    res_none = analyze_headline_sentiment(None)
    assert res_none["sentiment_score"] == 0.0
    assert res_none["sentiment_label"] == "Neutral"

    res_invalid_type = analyze_headline_sentiment(12345)  # type: ignore
    assert res_invalid_type["sentiment_score"] == 0.0
    assert res_invalid_type["sentiment_label"] == "Neutral"


def test_multiple_news_articles():
    """Test that multiple articles are all properly enriched with sentiment fields."""
    sample_articles = [
        {
            "title": "HDFC Bank posts fantastic earnings growth and strong revenue surge",
            "link": "https://example.com/1",
            "published": "2026-09-19",
            "source": "Financial Express"
        },
        {
            "title": "Major default warning issued as debt crisis deepens with terrible outlook",
            "link": "https://example.com/2",
            "published": "2026-09-18",
            "source": "Mint"
        },
        {
            "title": "TCS scheduled corporate governance meeting announced for next month",
            "link": "https://example.com/3",
            "published": "2026-09-17",
            "source": "Economic Times"
        },
        {
            # Malformed article with empty title
            "title": "",
            "link": "https://example.com/4",
            "published": "2026-09-16",
            "source": "Reuters"
        }
    ]

    enriched = analyze_news_sentiment(sample_articles)

    assert len(enriched) == 4
    for article in enriched:
        assert "sentiment_score" in article
        assert "sentiment_label" in article
        assert article["sentiment_label"] in ["Positive", "Negative", "Neutral"]
        assert isinstance(article["sentiment_score"], float)

    # First is positive, second is negative, third is neutral, fourth (empty) is neutral
    assert enriched[0]["sentiment_label"] == "Positive"
    assert enriched[1]["sentiment_label"] == "Negative"
    assert enriched[2]["sentiment_label"] == "Neutral"
    assert enriched[3]["sentiment_label"] == "Neutral"


def test_sentiment_summary_calculation():
    """Test aggregated counts, average score, and overall category calculation."""
    articles = [
        {"title": "Great news", "sentiment_score": 0.8, "sentiment_label": "Positive"},
        {"title": "More positive news", "sentiment_score": 0.6, "sentiment_label": "Positive"},
        {"title": "Neutral statement", "sentiment_score": 0.1, "sentiment_label": "Neutral"},
        {"title": "Terrible decline", "sentiment_score": -0.7, "sentiment_label": "Negative"},
    ]

    summary = calculate_sentiment_summary(articles)

    assert summary["total_articles"] == 4
    assert summary["positive_count"] == 2
    assert summary["neutral_count"] == 1
    assert summary["negative_count"] == 1

    # Expected average: (0.8 + 0.6 + 0.1 - 0.7) / 4 = 0.8 / 4 = 0.2
    assert summary["average_sentiment_score"] == 0.2
    assert summary["overall_sentiment"] == "Neutral"


def test_sentiment_summary_empty():
    """Test sentiment summary when article list is empty or None."""
    summary_empty = calculate_sentiment_summary([])
    assert summary_empty["total_articles"] == 0
    assert summary_empty["average_sentiment_score"] == 0.0
    assert summary_empty["overall_sentiment"] == "Neutral"

    summary_none = calculate_sentiment_summary(None)
    assert summary_none["total_articles"] == 0


def test_classification_threshold_boundaries():
    """Test strict Track A threshold boundary conditions."""
    assert classify_compound_score(0.5) == "Positive"
    assert classify_compound_score(0.5001) == "Positive"
    assert classify_compound_score(0.4999) == "Neutral"
    assert classify_compound_score(0.0) == "Neutral"
    assert classify_compound_score(-0.4999) == "Neutral"
    assert classify_compound_score(-0.5) == "Negative"
    assert classify_compound_score(-0.5001) == "Negative"
