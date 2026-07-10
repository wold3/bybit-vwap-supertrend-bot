import os

from dotenv import load_dotenv


# ==================================
# LOAD ENV
# ==================================

load_dotenv()



# ==================================
# BYBIT API
# ==================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)

BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)


BYBIT_BASE_URL = os.getenv(
    "BYBIT_BASE_URL",
    "https://api-demo.bybit.com"
)



# ==================================
# MODE
# ==================================

LIVE_TRADING = (
    os.getenv("LIVE_TRADING", "false")
    .lower()
    == "true"
)


BYBIT_TESTNET = (
    os.getenv("BYBIT_TESTNET", "false")
    .lower()
    == "true"
)


BYBIT_DEMO = (
    "demo" in BYBIT_BASE_URL.lower()
)



# ==================================
# WEBSOCKET
# ==================================

BYBIT_PUBLIC_WS = os.getenv(
    "BYBIT_PUBLIC_WS",
    "wss://stream.bybit.com/v5/public"
)


BYBIT_PRIVATE_WS = os.getenv(
    "BYBIT_PRIVATE_WS",
    "wss://stream-demo.bybit.com/v5/private"
)



# ==================================
# ACCOUNT
# ==================================

ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
)


CATEGORY = os.getenv(
    "CATEGORY",
    "linear"
)



# ==================================
# SYMBOL
# ==================================

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



# ==================================
# ORDER
# ==================================

DEFAULT_QTY = float(
    os.getenv(
        "DEFAULT_QTY",
        "0.001"
    )
)


ORDER_TYPE = os.getenv(
    "ORDER_TYPE",
    "Market"
)


TIME_IN_FORCE = os.getenv(
    "TIME_IN_FORCE",
    "GTC"
)


ORDER_COOLDOWN = int(
    os.getenv(
        "ORDER_COOLDOWN",
        "60"
    )
)


ORDER_RETRY = int(
    os.getenv(
        "ORDER_RETRY",
        "3"
    )
)



# ==================================
# LEVERAGE
# ==================================

LEVERAGE = int(
    os.getenv(
        "LEVERAGE",
        "3"
    )
)



# ==================================
# RISK
# ==================================

MAX_POSITION_SIZE = float(
    os.getenv(
        "MAX_POSITION_SIZE",
        "0.001"
    )
)


RISK_PER_TRADE_PERCENT = float(
    os.getenv(
        "RISK_PER_TRADE_PERCENT",
        "1.0"
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
        "5"
    )
)


MAX_LOSS_STREAK = int(
    os.getenv(
        "MAX_LOSS_STREAK",
        "3"
    )
)



# ==================================
# TP / SL
# ==================================

TAKE_PROFIT_PERCENT = float(
    os.getenv(
        "TAKE_PROFIT_PERCENT",
        "1.0"
    )
)


STOP_LOSS_PERCENT = float(
    os.getenv(
        "STOP_LOSS_PERCENT",
        "0.5"
    )
)



# ==================================
# INDICATOR
# ==================================

VWAP_LENGTH = int(
    os.getenv(
        "VWAP_LENGTH",
        "20"
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



# ==================================
# STRATEGY COMPATIBILITY
# ==================================

ST_LENGTH = SUPERTREND_PERIOD

ST_PERIOD = SUPERTREND_PERIOD

ST_MULTIPLIER = SUPERTREND_MULTIPLIER



# ==================================
# STRATEGY FILTER
# ==================================

USE_VOLUME_FILTER = (
    os.getenv(
        "USE_VOLUME_FILTER",
        "true"
    ).lower()
    == "true"
)


USE_VWAP_FILTER = (
    os.getenv(
        "USE_VWAP_FILTER",
        "true"
    ).lower()
    == "true"
)


USE_TREND_FILTER = (
    os.getenv(
        "USE_TREND_FILTER",
        "true"
    ).lower()
    == "true"
)


MIN_VOLUME = float(
    os.getenv(
        "MIN_VOLUME",
        "0"
    )
)


MIN_VOLUME_MULTIPLIER = float(
    os.getenv(
        "MIN_VOLUME_MULTIPLIER",
        "1.0"
    )
)


MIN_TREND_STRENGTH = float(
    os.getenv(
        "MIN_TREND_STRENGTH",
        "0.001"
    )
)



# ==================================
# WATCHDOG
# ==================================

WATCHDOG_INTERVAL = int(
    os.getenv(
        "WATCHDOG_INTERVAL",
        "30"
    )
)


WATCHDOG_TIMEOUT = int(
    os.getenv(
        "WATCHDOG_TIMEOUT",
        "120"
    )
)


MAX_API_ERROR = int(
    os.getenv(
        "MAX_API_ERROR",
        "5"
    )
)


MAX_HEARTBEAT_DELAY = int(
    os.getenv(
        "MAX_HEARTBEAT_DELAY",
        "180"
    )
)



# ==================================
# TELEGRAM
# ==================================

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
)


TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)



# ==================================
# DATABASE
# ==================================

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/bot.db"
)


DB_NAME = os.getenv(
    "DB_NAME",
    "bot.db"
)



# ==================================
# LOG
# ==================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)



# ==================================
# DEBUG
# ==================================

print("==============================")
print("[CONFIG LOADED]")
print("LIVE :", LIVE_TRADING)
print("DEMO :", BYBIT_DEMO)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")
