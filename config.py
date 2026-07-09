import os
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# MODE
# =====================================================

LIVE_TRADING = (
    os.getenv("LIVE_TRADING", "False").lower() == "true"
)

TESTNET = (
    os.getenv("TESTNET", "False").lower() == "true"
)


# =====================================================
# API
# =====================================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)

BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)


# =====================================================
# ACCOUNT
# =====================================================

ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
)

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)


# =====================================================
# REST API URL
# =====================================================

if LIVE_TRADING:

    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )

else:

    BYBIT_BASE_URL = (
        "https://api-demo.bybit.com"
    )


# =====================================================
# WEBSOCKET URL
# =====================================================

if LIVE_TRADING:

    PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public/linear"
    )

    PRIVATE_WS = (
        "wss://stream.bybit.com/v5/private"
    )

else:

    PUBLIC_WS = (
        "wss://stream-demo.bybit.com/v5/public/linear"
    )

    PRIVATE_WS = (
        "wss://stream-demo.bybit.com/v5/private"
    )


BYBIT_PUBLIC_WS = PUBLIC_WS
BYBIT_PRIVATE_WS = PRIVATE_WS


# =====================================================
# ORDER SETTINGS
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


# =====================================================
# RISK MANAGEMENT
# =====================================================

DAILY_LOSS_LIMIT = float(
    os.getenv(
        "DAILY_LOSS_LIMIT",
        "-100"
    )
)

ORDER_COOLDOWN = int(
    os.getenv(
        "ORDER_COOLDOWN",
        "30"
    )
)


# =====================================================
# STRATEGY SETTINGS
# =====================================================

TIMEFRAME = os.getenv(
    "TIMEFRAME",
    "5"
)

VWAP_ENABLED = True

SUPERTREND_ENABLED = True


# =====================================================
# LOG
# =====================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)


# =====================================================
# CONFIG CHECK
# =====================================================

print("==============================")
print("[CONFIG LOAD]")
print("------------------------------")
print("LIVE_TRADING :", LIVE_TRADING)
print("TESTNET      :", TESTNET)
print("BASE URL     :", BYBIT_BASE_URL)
print("------------------------------")
print("PUBLIC WS    :", BYBIT_PUBLIC_WS)
print("PRIVATE WS   :", BYBIT_PRIVATE_WS)
print("------------------------------")
print("SYMBOL       :", DEFAULT_SYMBOL)
print("ACCOUNT      :", ACCOUNT_TYPE)
print("TIMEFRAME    :", TIMEFRAME)
print("------------------------------")
print(
    "API KEY      :",
    BYBIT_API_KEY[:6] if BYBIT_API_KEY else "EMPTY"
)
print("==============================")
