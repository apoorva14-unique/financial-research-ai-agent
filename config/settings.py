"""
Global Application Settings and Configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "finance.db"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Application Meta
APP_TITLE = "Financial Research & Analytics AI Agent"
APP_SUBTITLE = "Indian Stock Analysis Assistant (NSE & BSE)"
APP_ICON = "📈"
APP_LAYOUT = "wide"

# Default Indian Stock Tickers (NSE Symbols)
DEFAULT_TICKERS = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "TATAMOTORS.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
]

# Database Settings
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH.as_posix()}")

# Regulatory & Compliance Disclaimer
SEBI_DISCLAIMER = (
    "DISCLAIMER: This application is for educational and research purposes only. "
    "It is not registered with SEBI as an investment advisor. The information and analytics "
    "presented do not constitute financial advice or recommendations to buy or sell securities. "
    "Always consult a certified financial advisor before making investment decisions."
)
