# =====================================================
# config.py
# GLOBAL BOT CONFIG
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


BYBIT_REST_URL = os.getenv(
    "BYBIT_REST_URL",
    "https://api-demo.bybit.com"
)


BYBIT_PRIVATE_WS = os.getenv(
    "BYBIT_PRIVATE_WS",
    "wss://stream-demo.bybit.com/v5/private"
)





# =====================================================
# ACCOUNT / MARKET
# =====================================================

CATEGORY = "linear"

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)


ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
)





# =====================================================
# LEVERAGE
# =====================================================

LEVERAGE = int(
    os.getenv(
        "LEVERAGE",
        "5"
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





# =====================================================
# RISK MANAGEMENT
# =====================================================

RISK_PER_TRADE_PERCENT = float(
    os.getenv(
        "RISK_PER_TRADE_PERCENT",
        "1"
    )
)


MAX_POSITION_SIZE = float(
    os.getenv(
        "MAX_POSITION_SIZE",
        "0.01"
    )
)


MAX_DAILY_LOSS_PERCENT = float(
    os.getenv(
        "MAX_DAILY_LOSS_PERCENT",
        "5"
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
        "3"
    )
)


ORDER_COOLDOWN = int(
    os.getenv(
        "ORDER_COOLDOWN",
        "300"
    )
)





# =====================================================
# TP / SL
# =====================================================

STOP_LOSS_PERCENT = float(
    os.getenv(
        "STOP_LOSS_PERCENT",
        "1"
    )
)


TAKE_PROFIT_PERCENT = float(
    os.getenv(
        "TAKE_PROFIT_PERCENT",
        "2"
    )
)





# =====================================================
# INDICATORS
# =====================================================

ATR_PERIOD = int(
    os.getenv(
        "ATR_PERIOD",
        "14"
    )
)


SUPERTREND_MULTIPLIER = float(
    os.getenv(
        "SUPERTREND_MULTIPLIER",
        "3"
    )
)





# =====================================================
# VWAP / VOLUME FILTER
# =====================================================

USE_VOLUME_FILTER = (
    os.getenv(
        "USE_VOLUME_FILTER",
        "True"
    )
    .lower()
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
# TELEGRAM
# =====================================================

TELEGRAM_ENABLED = (
    os.getenv(
        "TELEGRAM_ENABLED",
        "False"
    )
    .lower()
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

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/trading.db"
)





# =====================================================
# LOG
# =====================================================

LIVE_TRADING = (
    os.getenv(
        "LIVE_TRADING",
        "False"
    )
    .lower()
    == "true"
)





print("==============================")
print("[CONFIG LOADED]")
print("LIVE :", LIVE_TRADING)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("LEVERAGE :", LEVERAGE)
print("==============================")
