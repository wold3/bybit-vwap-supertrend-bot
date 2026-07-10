import os
from dotenv import load_dotenv


# ==================================
# ENV LOAD
# ==================================

load_dotenv(
    override=True
)


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


# ==================================
# SERVER
# ==================================

BYBIT_BASE_URL = os.getenv(
    "BYBIT_BASE_URL",
    "https://api-demo.bybit.com"
)


BYBIT_PUBLIC_WS = os.getenv(
    "BYBIT_PUBLIC_WS",
    "wss://stream.bybit.com/v5/public"
)


BYBIT_PRIVATE_WS = os.getenv(
    "BYBIT_PRIVATE_WS",
    "wss://stream-demo.bybit.com/v5/private"
)


# ==================================
# MODE
# ==================================

LIVE_TRADING = (
    os.getenv(
        "LIVE_TRADING",
        "false"
    ).lower()
    == "true"
)


BYBIT_TESTNET = (
    os.getenv(
        "BYBIT_TESTNET",
        "false"
    ).lower()
    == "true"
)


DEMO = not LIVE_TRADING

TESTNET = BYBIT_TESTNET


# ==================================
# ACCOUNT
# ==================================

ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
)


# ==================================
# MARKET
# ==================================

CATEGORY = os.getenv(
    "CATEGORY",
    "linear"
)


DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)


# ==================================
# ORDER
# ==================================

ORDER_RETRY = int(
    os.getenv(
        "ORDER_RETRY",
        "3"
    )
)


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


LEVERAGE = int(
    os.getenv(
        "LEVERAGE",
        "3"
    )
)


# ==================================
# INDICATORS
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
        "3.0"
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


# 호환용
MAX_POSITION = MAX_POSITION_SIZE


MAX_DAILY_LOSS = float(
    os.getenv(
        "MAX_DAILY_LOSS",
        "0.03"
    )
)


MAX_LOSS_AMOUNT = float(
    os.getenv(
        "MAX_LOSS_AMOUNT",
        "0"
    )
)


RISK_PERCENT = float(
    os.getenv(
        "RISK_PERCENT",
        "1.0"
    )
)


STOP_LOSS_PERCENT = float(
    os.getenv(
        "STOP_LOSS_PERCENT",
        "1.0"
    )
)


TAKE_PROFIT_PERCENT = float(
    os.getenv(
        "TAKE_PROFIT_PERCENT",
        "2.0"
    )
)


MAX_OPEN_POSITIONS = int(
    os.getenv(
        "MAX_OPEN_POSITIONS",
        "1"
    )
)


# ==================================
# LOG
# ==================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)


# ==================================
# STATUS
# ==================================

print("==============================")
print("[CONFIG LOADED]")
print("DEMO :", DEMO)
print("TESTNET :", TESTNET)
print("LIVE :", LIVE_TRADING)
print("ACCOUNT :", ACCOUNT_TYPE)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("QTY :", DEFAULT_QTY)
print("LEVERAGE :", LEVERAGE)
print("VWAP :", VWAP_LENGTH)
print("SUPERTREND :", SUPERTREND_PERIOD, SUPERTREND_MULTIPLIER)
print("REST :", BYBIT_BASE_URL)
print("PUBLIC WS :", BYBIT_PUBLIC_WS)
print("PRIVATE WS :", BYBIT_PRIVATE_WS)
print("==============================")
