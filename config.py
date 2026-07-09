# config.py

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
# SERVER MODE
# ==================================

BYBIT_TESTNET = (
    os.getenv(
        "BYBIT_TESTNET",
        "false"
    ).lower()
    == "true"
)


LIVE_TRADING = (
    os.getenv(
        "LIVE_TRADING",
        "false"
    ).lower()
    == "true"
)


# ==================================
# BASE URL
# ==================================

if BYBIT_TESTNET:

    BYBIT_BASE_URL = (
        "https://api-testnet.bybit.com"
    )

else:

    BYBIT_BASE_URL = os.getenv(
        "BYBIT_BASE_URL",
        "https://api.bybit.com"
    )



# ==================================
# WEBSOCKET
# ==================================

if BYBIT_TESTNET:

    BYBIT_PUBLIC_WS = (
        "wss://stream-testnet.bybit.com/v5/public/linear"
    )

    BYBIT_PRIVATE_WS = (
        "wss://stream-testnet.bybit.com/v5/private"
    )

else:

    BYBIT_PUBLIC_WS = os.getenv(
        "BYBIT_PUBLIC_WS",
        "wss://stream.bybit.com/v5/public/linear"
    )

    BYBIT_PRIVATE_WS = os.getenv(
        "BYBIT_PRIVATE_WS",
        "wss://stream.bybit.com/v5/private"
    )



# ==================================
# SYMBOL
# ==================================

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



# ==================================
# ACCOUNT
# ==================================

ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
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
# DEBUG
# ==================================

print("==============================")
print("[CONFIG LOAD]")
print("LIVE_TRADING :", LIVE_TRADING)
print("TESTNET      :", BYBIT_TESTNET)
print("BASE URL     :", BYBIT_BASE_URL)
print("PUBLIC WS    :", BYBIT_PUBLIC_WS)
print("PRIVATE WS   :", BYBIT_PRIVATE_WS)
print("SYMBOL       :", DEFAULT_SYMBOL)
print("ACCOUNT      :", ACCOUNT_TYPE)

if BYBIT_API_KEY:
    print(
        "API KEY      :",
        BYBIT_API_KEY[:6]
    )
else:
    print(
        "API KEY      : NONE"
    )

print("==============================")
