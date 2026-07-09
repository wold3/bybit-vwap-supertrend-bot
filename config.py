import os
from dotenv import load_dotenv

load_dotenv(".env")


# ================================
# API
# ================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)

BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)


# ================================
# MODE
# ================================

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


# ================================
# SERVER
# ================================

BYBIT_BASE_URL = os.getenv(
    "BYBIT_BASE_URL",
    "https://api-demo.bybit.com"
)


# ================================
# WS
# ================================

BYBIT_PUBLIC_WS = os.getenv(
    "BYBIT_PUBLIC_WS",
    "wss://stream-demo.bybit.com/v5/public/linear"
)


BYBIT_PRIVATE_WS = os.getenv(
    "BYBIT_PRIVATE_WS",
    "wss://stream-demo.bybit.com/v5/private"
)


# ================================
# TRADING
# ================================

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)


ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
)


ORDER_RETRY = int(
    os.getenv(
        "ORDER_RETRY",
        "3"
    )
)


LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)


# ================================
# DEBUG
# ================================

print("==============================")
print("[CONFIG LOAD]")
print("LIVE_TRADING :", LIVE_TRADING)
print("TESTNET      :", BYBIT_TESTNET)
print("BASE URL     :", BYBIT_BASE_URL)
print("PUBLIC WS    :", BYBIT_PUBLIC_WS)
print("PRIVATE WS   :", BYBIT_PRIVATE_WS)
print("SYMBOL       :", DEFAULT_SYMBOL)
print("ACCOUNT      :", ACCOUNT_TYPE)
print(
    "API KEY      :",
    BYBIT_API_KEY[:6]
)
print("==============================")
