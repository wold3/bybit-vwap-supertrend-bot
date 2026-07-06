import os
from dotenv import load_dotenv

load_dotenv()


# =====================================================
# BYBIT
# =====================================================

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
BYBIT_TESTNET = os.getenv("BYBIT_TESTNET", "true").lower() == "true"


# =====================================================
# TELEGRAM
# =====================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# =====================================================
# DATABASE
# =====================================================

DB_TYPE = os.getenv("DB_TYPE", "sqlite")

SQLITE_PATH = os.getenv("SQLITE_PATH", "./data/trading.db")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# =====================================================
# TRADING
# =====================================================

SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1m")

INITIAL_EQUITY = float(os.getenv("INITIAL_EQUITY", 1000))


# =====================================================
# RISK
# =====================================================

MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", 50))
MAX_LOSS_STREAK = int(os.getenv("MAX_LOSS_STREAK", 5))

BASE_RISK = float(os.getenv("BASE_RISK", 0.02))


# =====================================================
# EXECUTION
# =====================================================

LEVERAGE_MAX = int(os.getenv("LEVERAGE_MAX", 5))
SLIPPAGE_BUFFER = float(os.getenv("SLIPPAGE_BUFFER", 0.0003))
FEE_RATE = float(os.getenv("FEE_RATE", 0.0006))
