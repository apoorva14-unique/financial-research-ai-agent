import json
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from agent.tools import (
    fundamentals_tool,
    news_tool,
    stock_price_tool,
    technical_analysis_tool,
)

# Ensure environment variables are loaded
load_dotenv()

logger = logging.getLogger(__name__)

# Default model on Groq with verified function-calling capability
PRIMARY_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
FALLBACK_MODEL = "openai/gpt-oss-120b"


# =====================================================================
# 1. TOOL DEFINITIONS (Decorated with LangChain @tool)
# =====================================================================

@tool
def get_stock_price(ticker: str) -> Dict[str, Any]:
    """Get current stock price, day high, day low, and trading volume for an Indian equity symbol (e.g., 'RELIANCE.NS', 'TCS.NS', 'INFY.NS')."""
    return stock_price_tool(ticker)


@tool
def get_technical_analysis(ticker: str) -> Dict[str, Any]:
    """Get technical indicators including RSI (14-day), SMA 20, SMA 50, EMA 20, MACD, and MACD signal for an equity symbol (e.g., 'RELIANCE.NS')."""
    return technical_analysis_tool(ticker)


@tool
def get_fundamental_analysis(ticker: str) -> Dict[str, Any]:
    """Get fundamental financial metrics including P/E ratio, P/B ratio, ROE, Profit Margin, Market Cap, Sector, and Industry for an equity symbol."""
    return fundamentals_tool(ticker)


@tool
def get_news(company_name: str) -> List[Dict[str, str]]:
    """Get recent financial news articles and headlines for a company name (e.g., 'Reliance Industries', 'Tata Consultancy Services', 'HDFC Bank')."""
    return news_tool(company_name)


# Registered agent tool list and lookup mapping
TOOLS = [
    get_stock_price,
    get_technical_analysis,
    get_fundamental_analysis,
    get_news,
]
TOOL_MAP = {t.name: t for t in TOOLS}


# =====================================================================
# 2. SYSTEM INSTRUCTIONS FOR THE FINANCIAL ANALYST AGENT
# =====================================================================

SYSTEM_PROMPT = """You are an expert AI Financial Research Analyst specializing in Indian equity markets (NSE/BSE).
Your task is to answer user queries accurately using real-time and historical financial data retrieved via your tools.

Available Tools:
1. `get_stock_price`: Fetches current price, daily high, daily low, and volume.
2. `get_technical_analysis`: Fetches RSI, SMA 20, SMA 50, EMA 20, and MACD indicators.
3. `get_fundamental_analysis`: Fetches valuation ratios (P/E, P/B), profitability (ROE, profit margin), market cap, and sector.
4. `get_news`: Fetches latest headlines and market news for a company.

Guidelines:
- ALWAYS use the relevant tool(s) to fetch data before answering. Do not guess or fabricate financial numbers.
- For Indian stocks, if the user does not specify an exchange suffix, assume NSE (e.g., 'RELIANCE.NS', 'TCS.NS', 'INFY.NS').
- If the user asks for a specific topic (e.g. price, technicals, fundamentals, or news), invoke the corresponding tool.
- If the user asks for a comprehensive research summary, investment overview, or combined analysis:
  1. Fetch price data (`get_stock_price`).
  2. Fetch technical indicators (`get_technical_analysis`).
  3. Fetch fundamental metrics (`get_fundamental_analysis`).
  4. Fetch recent news (`get_news`).
  5. Synthesize a professional report with:
     - Executive Summary & Current Market Price
     - Technical Indicator Analysis & Trend Interpretation
     - Fundamental Valuation & Financial Health
     - Recent News & Sentiment Analysis
     - Research Takeaway & Risk Factors
- Always conclude with the mandatory compliance disclaimer:
  "Educational & Research Purpose Only. This tool is not a SEBI registered investment advisor. The information does not constitute financial advice."
"""


# =====================================================================
# 3. AGENT INITIALIZATION & FACTORY
# =====================================================================

def create_agent(model_name: Optional[str] = None):
    """
    Creates and returns the LangChain Groq Chat model bound to the financial research tools.
    Supports graceful fallback if a model is unavailable on the user's Groq tier.
    """
    selected_model = model_name or PRIMARY_MODEL

    try:
        llm = ChatGroq(
            model=selected_model,
            temperature=0,
        )
        return llm.bind_tools(TOOLS)
    except Exception as e:
        logger.warning(
            f"Failed initializing model '{selected_model}' ({e}); attempting fallback to '{FALLBACK_MODEL}'."
        )
        llm = ChatGroq(
            model=FALLBACK_MODEL,
            temperature=0,
        )
        return llm.bind_tools(TOOLS)


# =====================================================================
# 4. REACT AGENT EXECUTION LOOP (VIVA-READY & TRANSPARENT)
# =====================================================================

def run_agent(query: str, max_iterations: int = 6) -> str:
    """
    Accepts a user question and executes a complete ReAct (Reasoning + Acting) loop:
    1. Sends the query to the Groq LLM equipped with financial tools.
    2. Inspects model response for tool calls.
    3. Executes each requested tool and appends a ToolMessage observation.
    4. Feeds observations back to the LLM to continue reasoning or generate final answer.
    5. Returns the synthesized AI answer string. Handles all errors gracefully.
    """
    if not query or not query.strip():
        return "Please enter a valid stock question or ticker symbol."

    try:
        # Initialize model with tools
        llm_with_tools = create_agent()

        # Conversation history initialized with system persona and user prompt
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query.strip()),
        ]

        # Iterative ReAct loop
        for step in range(max_iterations):
            try:
                ai_response: AIMessage = llm_with_tools.invoke(messages)
            except Exception as llm_err:
                # Handle model-specific errors (e.g., 404 or decommissioned model fallback)
                err_str = str(llm_err)
                if "model_not_found" in err_str or "model_decommissioned" in err_str:
                    logger.warning(f"Model error encountered: {err_str}. Retrying with fallback model.")
                    llm_with_tools = ChatGroq(model=FALLBACK_MODEL, temperature=0).bind_tools(TOOLS)
                    ai_response = llm_with_tools.invoke(messages)
                else:
                    raise llm_err

            messages.append(ai_response)

            # Check if LLM decided to call any tools
            tool_calls = getattr(ai_response, "tool_calls", None)

            # If no tools were called, the LLM has produced its final synthesized answer
            if not tool_calls:
                return ai_response.content

            # Execute each requested tool call
            for tc in tool_calls:
                tool_name = tc.get("name")
                tool_args = tc.get("args", {})
                call_id = tc.get("id", f"call_{step}")

                tool_fn = TOOL_MAP.get(tool_name)
                if tool_fn is not None:
                    try:
                        tool_result = tool_fn.invoke(tool_args)
                    except Exception as tool_exec_err:
                        tool_result = {
                            "error": f"Tool '{tool_name}' failed to execute: {str(tool_exec_err)}"
                        }
                else:
                    tool_result = {"error": f"Tool '{tool_name}' is not recognized."}

                # Format result for the LLM
                content_str = (
                    json.dumps(tool_result, ensure_ascii=False)
                    if isinstance(tool_result, (dict, list))
                    else str(tool_result)
                )

                messages.append(
                    ToolMessage(content=content_str, tool_call_id=call_id)
                )

        # If loop reached max iterations without concluding, request a final synthesis
        final_prompt = messages + [
            HumanMessage(content="Please provide the final synthesized response based on the data retrieved so far.")
        ]
        final_ai = llm_with_tools.invoke(final_prompt)
        return final_ai.content

    except Exception as e:
        logger.error(f"Error in run_agent: {e}", exc_info=True)
        return (
            f"An error occurred while processing your request: {str(e)}\n\n"
            "Please check that your Groq API key is valid and your network connection is active."
        )


# Clean alias for convenience
ask_agent = run_agent