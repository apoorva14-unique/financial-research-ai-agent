"""
Live integration verification script for Financial Research AI Agent.
Tests all 5 required query categories:
1. Current stock price
2. Technical indicators
3. Fundamentals
4. Recent financial news
5. Combined stock research summary
"""

import sys
from agent.agent_core import run_agent

queries = [
    ("1. Stock Price", "What is the current stock price of Reliance?"),
    ("2. Technical Indicators", "What is the RSI and MACD for TCS?"),
    ("3. Fundamentals", "What is the P/E ratio, Market Cap, and ROE of Infosys?"),
    ("4. News", "What is the latest financial news for Tata Motors?"),
    ("5. Combined Research Summary", "Provide a concise combined research summary for HDFCBANK including price, technicals, and fundamentals."),
]

def main():
    print("=" * 60)
    print("STARTING FINANCIAL AI AGENT LIVE VERIFICATION")
    print("=" * 60)

    for label, q in queries:
        print(f"\n--- Testing: {label} ---")
        print(f"User Query: {q}")
        try:
            answer = run_agent(q)
            # Safe print to handle any terminal encodings
            safe_output = answer.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8")
            print("AI Answer:\n", safe_output[:350] + ("..." if len(safe_output) > 350 else ""))
            print(f"-> {label} PASSED!")
        except Exception as e:
            print(f"-> {label} FAILED with exception: {e}")
            return 1

    print("\n" + "=" * 60)
    print("ALL 5 LIVE AGENT TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
