# config.py

import os
from dotenv import load_dotenv

load_dotenv()


# =====================================================
# MODE
# =====================================================

LIVE = (
    os.getenv("LIVE", "False")
    .lower()
    == "true"
)

DEMO = (
    os.getenv("DEMO", "True")
    .lower()
    == "true"
)



# =====================================================
# BYBIT API
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
    os.getenv("BYBIT_TESTNET", "False")
    .lower()
    == "true"
)


BYBIT_DEMO = (
    os.getenv("BYBIT_DEMO", "True")
    .lower()
    == "true"
)



# =====================================================
# ACCOUNT / MARKET
# =====================================================

ACCOUNT_TYPE = "UNIFIED"

CATEGORY = os.getenv(
    "CATEGORY",
    "linear"
)


DEFAULT_SYMBOL = os.getenv(
    "SYMBOL",
    "BTCUSDT"
)


SYMBOL = DEFAULT_SYMBOL



# =====================================================
# ORDER SETTINGS
# =====================================================

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


MAX_POSITION_SIZE = float(
    os.getenv(
        "MAX_POSITION_SIZE",
        "0.01"
    )
)


ORDER_COOLDOWN = int(
    os.getenv(
        "ORDER_COOLDOWN",
        "60"
    )
)



# =====================================================
# VWAP SETTINGS
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
        "True"
    )
    .lower()
    ==
    "true"
)


MIN_VOLUME_MULTIPLIER = float(
    os.getenv(
        "MIN_VOLUME_MULTIPLIER",
        "1.2"
    )
)



# =====================================================
# SUPERTREND SETTINGS
# =====================================================

ST_LENGTH = int(
    os.getenv(
        "ST_LENGTH",
        "10"
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


MAX_DAILY_LOSS_PERCENT = float(
    os.getenv(
        "MAX_DAILY_LOSS_PERCENT",
        "5"
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
        "False"
    )
    .lower()
    ==
    "true"
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


DATABASE_FILE = DATABASE_PATH



# =====================================================
# LOOP
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
# DEBUG
# =====================================================

DEBUG = (
    os.getenv(
        "DEBUG",
        "False"
    )
    .lower()
    ==
    "true"
)



print("==============================")
print("[CONFIG LOADED]")
print("LIVE :", LIVE)
print("DEMO :", DEMO)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")
