# =====================================================
# config.py
# Bybit VWAP SuperTrend Bot Configuration
# =====================================================

import os
from dotenv import load_dotenv

load_dotenv()


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


# =====================================================
# ACCOUNT / MARKET
# =====================================================

CATEGORY = os.getenv(
    "CATEGORY",
    "linear"
)


DEFAULT_SYMBOL = os.getenv(
    "SYMBOL",
    "BTCUSDT"
)


ACCOUNT_TYPE = "UNIFIED"


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
# ORDER
# =====================================================

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
        "3"
    )
)



# =====================================================
# STRATEGY
# =====================================================

VWAP_LENGTH = int(
    os.getenv(
        "VWAP_LENGTH",
        "50"
    )
)


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
# PRIVATE WEBSOCKET
# =====================================================

BYBIT_PRIVATE_WS = (
    "wss://stream.bybit.com/v5/private"
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
# BOT MODE
# =====================================================

LIVE = (
    os.getenv(
        "LIVE",
        "false"
    ).lower()
    == "true"
)


DEMO = (
    os.getenv(
        "DEMO",
        "true"
    ).lower()
    == "true"
)



# =====================================================
# DEBUG
# =====================================================

DEBUG = True



print("==============================")
print("[CONFIG LOADED]")
print("LIVE :", LIVE)
print("DEMO :", DEMO)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")
