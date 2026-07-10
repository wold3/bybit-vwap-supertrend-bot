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
        "false"
    ).lower()
    == "true"
)


BYBIT_DEMO = (
    os.getenv(
        "BYBIT_DEMO",
        "true"
    ).lower()
    == "true"
)



CATEGORY = os.getenv(
    "CATEGORY",
    "linear"
)


DEFAULT_SYMBOL = os.getenv(
    "SYMBOL",
    "BTCUSDT"
)



# =====================================================
# ACCOUNT
# =====================================================

ACCOUNT_TYPE = "UNIFIED"



# =====================================================
# TRADING
# =====================================================

LIVE = (
    os.getenv(
        "LIVE",
        "false"
    ).lower()
    == "true"
)


DEMO = BYBIT_DEMO



LEVERAGE = int(
    os.getenv(
        "LEVERAGE",
        "3"
    )
)



DEFAULT_QTY = float(
    os.getenv(
        "DEFAULT_QTY",
        "0.001"
    )
)



# =====================================================
# VWAP
# =====================================================

VWAP_LENGTH = int(
    os.getenv(
        "VWAP_LENGTH",
        "50"
    )
)


USE_VOLUME_FILTER = (
    os.getenv(
        "USE_VOLUME_FILTER",
        "true"
    ).lower()
    == "true"
)


MIN_VOLUME_MULTIPLIER = float(
    os.getenv(
        "MIN_VOLUME_MULTIPLIER",
        "1.2"
    )
)



# =====================================================
# SUPERTREND
# =====================================================

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


ST_LENGTH = SUPERTREND_PERIOD

ST_MULTIPLIER = SUPERTREND_MULTIPLIER



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
# TELEGRAM
# =====================================================

TELEGRAM_ENABLED = (
    os.getenv(
        "TELEGRAM_ENABLED",
        "false"
    ).lower()
    == "true"
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
# DATABASE
# =====================================================

DATABASE_ENABLED = True


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "trading.db"
)



# =====================================================
# DEBUG
# =====================================================

DEBUG = (
    os.getenv(
        "DEBUG",
        "false"
    ).lower()
    == "true"
)



print("==============================")
print("[CONFIG LOADED]")
print("LIVE :", LIVE)
print("DEMO :", DEMO)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")
