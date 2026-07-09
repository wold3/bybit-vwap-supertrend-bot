# =========================================================
# CONFIGURATION
# BYBIT VWAP SUPERTREND BOT
# =========================================================

import os
from dotenv import load_dotenv


load_dotenv()



# =========================================================
# ENV
# =========================================================

ENV = os.getenv(
    "ENV",
    "DEMO"
)



# =========================================================
# BYBIT API
# =========================================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)



# =========================================================
# NETWORK
# =========================================================

BYBIT_TESTNET = os.getenv(
    "BYBIT_TESTNET",
    "True"
).lower() == "true"



if BYBIT_TESTNET:

    BYBIT_BASE_URL = (
        "https://api-demo.bybit.com"
    )

    BYBIT_PUBLIC_WS = (
        "wss://stream-demo.bybit.com/v5/public/linear"
    )

    BYBIT_PRIVATE_WS = (
        "wss://stream-demo.bybit.com/v5/private"
    )


else:

    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )

    BYBIT_PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public/linear"
    )

    BYBIT_PRIVATE_WS = (
        "wss://stream.bybit.com/v5/private"
    )



# =========================================================
# ACCOUNT
# =========================================================

# Bybit Unified Trading Account
ACCOUNT_TYPE = "UNIFIED"


# Linear USDT Perpetual
CATEGORY = "linear"


SETTLE_COIN = "USDT"



# =========================================================
# SYMBOL
# =========================================================

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



# =========================================================
# TRADING MODE
# =========================================================

LIVE_TRADING = os.getenv(
    "LIVE_TRADING",
    "False"
).lower() == "true"



# 기본 주문 수량
DEFAULT_QTY = float(
    os.getenv(
        "DEFAULT_QTY",
        "0.001"
    )
)



# =========================================================
# STRATEGY
# =========================================================

TIMEFRAME = "1"


# VWAP
VWAP_LENGTH = 50


# Supertrend
SUPERTREND_PERIOD = 10

SUPERTREND_MULTIPLIER = 3



# =========================================================
# RISK MANAGEMENT
# =========================================================

MAX_POSITION_SIZE = float(
    os.getenv(
        "MAX_POSITION_SIZE",
        "0.01"
    )
)


ORDER_COOLDOWN = int(
    os.getenv(
        "ORDER_COOLDOWN",
        "30"
    )
)


DAILY_LOSS_LIMIT = float(
    os.getenv(
        "DAILY_LOSS_LIMIT",
        "-100"
    )
)



# =========================================================
# SYSTEM
# =========================================================

LOG_LEVEL = "INFO"


HEARTBEAT_INTERVAL = 60


WATCHDOG_INTERVAL = 30



# =========================================================
# DATABASE
# =========================================================

TRADE_DB = "trades.db"

HISTORY_DB = "trade_history.db"



# =========================================================
# TELEGRAM (OPTIONAL)
# =========================================================

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
)


TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)



# =========================================================
# DEBUG
# =========================================================

print("==============================")
print("[CONFIG LOADED]")
print("ENV :", ENV)
print("TESTNET :", BYBIT_TESTNET)
print("BASE :", BYBIT_BASE_URL)
print("SYMBOL :", DEFAULT_SYMBOL)
print("LIVE :", LIVE_TRADING)
print("ACCOUNT :", ACCOUNT_TYPE)
print("==============================")
