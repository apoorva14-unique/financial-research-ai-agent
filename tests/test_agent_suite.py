"""
Unit and functional test suite for the Financial Research AI Agent.
Can be executed with pytest or standard unittest runner.
"""

import unittest
from agent.tools import (
    _normalize_ticker,
    stock_price_tool,
    technical_analysis_tool,
    fundamentals_tool,
    news_tool,
)
from agent.agent_core import create_agent, run_agent, TOOLS, TOOL_MAP


class TestAgentTools(unittest.TestCase):

    def test_normalize_ticker(self):
        self.assertEqual(_normalize_ticker("RELIANCE"), "RELIANCE.NS")
        self.assertEqual(_normalize_ticker("reliance"), "RELIANCE.NS")
        self.assertEqual(_normalize_ticker("TCS.NS"), "TCS.NS")
        self.assertEqual(_normalize_ticker("500325.BO"), "500325.BO")
        self.assertEqual(_normalize_ticker(""), "")

    def test_tools_registration(self):
        self.assertEqual(len(TOOLS), 4)
        expected_names = {
            "get_stock_price",
            "get_technical_analysis",
            "get_fundamental_analysis",
            "get_news",
        }
        self.assertEqual(set(TOOL_MAP.keys()), expected_names)

    def test_empty_query_handling(self):
        response = run_agent("")
        self.assertIn("valid", response.lower())

    def test_invalid_ticker_handling(self):
        result = stock_price_tool("NON_EXISTENT_SYMBOL_XYZ_123")
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
