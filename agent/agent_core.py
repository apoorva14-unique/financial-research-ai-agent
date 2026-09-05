import os

from langchain_groq import ChatGroq
from langchain_core.tools import tool


@tool
def get_stock_price(ticker: str):
    """Get the latest stock price and trading information."""

    from agent.tools import stock_price_tool

    return stock_price_tool(ticker)


@tool
def get_technical_analysis(ticker: str):
    """Get RSI, SMA, EMA and MACD technical indicators."""

    from agent.tools import technical_analysis_tool

    return technical_analysis_tool(ticker)


@tool
def get_fundamental_analysis(ticker: str):
    """Get company fundamental metrics."""

    from agent.tools import fundamentals_tool

    return fundamentals_tool(ticker)


@tool
def get_news(company_name: str):
    """Get recent financial news."""

    from agent.tools import news_tool

    return news_tool(company_name)


def create_agent():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    tools = [
        get_stock_price,
        get_technical_analysis,
        get_fundamental_analysis,
        get_news
    ]

    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools