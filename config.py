import os
from dotenv import load_dotenv

load_dotenv()


# =====================================================
# BYBIT
# =====================================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)

BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)


BYBIT_TESTNET = (
    os.getenv(
        "BYBIT_TESTNET",
        "False"
    ).lower() == "true"
)


BYBIT_DEMO = (
    os.getenv(
        "BYBIT_DEMO",
        "True"
    ).lower() == "true"
)



# =====================================================
# MARKET
# =====================================================

CATEGORY = "linear"

DEFAULT_SYMBOL = os.getenv(
    "SYMBOL",
    "BTCUSDT"
)



# =====================================================
# ACCOUNT
# =====================================================

ACCOUNT_TYPE = "UNIFIED"



# =====================================================
# TRADING MODE
# =====================================================

LIVE = (
    os.getenv(
        "LIVE",
        "False"
    ).lower() == "true"
)


DEMO = not LIVE



# =====================================================
# LEVERAGE
# =====================================================

LEVERAGE = int(
    os.getenv(
        "LEVERAGE",
        "3"
    )
)



# =====================================================
# STRATEGY
# VWAP + SUPERTREND
# =====================================================

VWAP_LENGTH = int(
    os.getenv(
        "VWAP_LENGTH",
        "50"
    )
)


SUPERTREND_PERIOD = int(
    os.getenv(
        "SUPERTREND_PERIOD",
        "10"
    )
)


SUPERTREND_MULTIPLIER = float(
    os.getenv(
        "SUPERTREND_MULTIPLIER",
        "3"
    )
)



# Volume Filter

USE_VOLUME_FILTER = (
    os.getenv(
        "USE_VOLUME_FILTER",
        "True"
    ).lower() == "true"
)


MIN_VOLUME_MULTIPLIER = float(
    os.getenv(
        "MIN_VOLUME_MULTIPLIER",
        "1.2"
    )
)



# =====================================================
# RISK MANAGEMENT
# =====================================================

RISK_PER_TRADE_PERCENT = float(
    os.getenv(
        "RISK_PER_TRADE_PERCENT",
        "1"
    )
)


MAX_DRAWDOWN_PERCENT = float(
    os.getenv(
        "MAX_DRAWDOWN_PERCENT",
        "10"
    )
)


MAX_LOSS_STREAK = int(
    os.getenv(
        "MAX_LOSS_STREAK",
        "5"
    )
)


MAX_POSITION_SIZE = float(
    os.getenv(
        "MAX_POSITION_SIZE",
        "0.01"
    )
)



# =====================================================
# WATCHDOG
# =====================================================

WATCHDOG_INTERVAL = int(
    os.getenv(
        "WATCHDOG_INTERVAL",
        "30"
    )
)


MAX_API_ERROR = int(
    os.getenv(
        "MAX_API_ERROR",
        "5"
    )
)



# =====================================================
# DATABASE
# =====================================================

DATABASE_ENABLED = True

DATABASE_FILE = "trading.db"



# =====================================================
# TELEGRAM
# =====================================================

TELEGRAM_ENABLED = (
    os.getenv(
        "TELEGRAM_ENABLED",
        "False"
    ).lower() == "true"
)


TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
)


TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)



# =====================================================
# BOT LOOP
# =====================================================

KLINE_INTERVAL = os.getenv(
    "KLINE_INTERVAL",
    "1"
)


LOOP_INTERVAL = int(
    os.getenv(
        "LOOP_INTERVAL",
        "5"
    )
)



# =====================================================
# LOG
# =====================================================

LOG_LEVEL = "INFO"



# =====================================================
# PRINT CHECK
# =====================================================

print("==============================")
print("[CONFIG LOADED]")
print("LIVE :", LIVE)
print("DEMO :", DEMO)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")
