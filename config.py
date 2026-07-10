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


# Demo Trading 여부

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
# SYMBOL
# ==================================

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


# ==================================
# LOG
# ==================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)


# ==================================
# PRINT STATUS
# ==================================

print("==============================")
print("[CONFIG LOADED]")
print("DEMO :", DEMO)
print("TESTNET :", TESTNET)
print("LIVE :", LIVE_TRADING)
print("ACCOUNT :", ACCOUNT_TYPE)
print("SYMBOL :", DEFAULT_SYMBOL)
print("REST :", BYBIT_BASE_URL)
print("PUBLIC WS :", BYBIT_PUBLIC_WS)
print("PRIVATE WS :", BYBIT_PRIVATE_WS)
print("==============================")
