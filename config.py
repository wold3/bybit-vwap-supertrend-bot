import os
from dotenv import load_dotenv


# ==========================================================
# ENV LOAD
# ==========================================================

load_dotenv()



# ==========================================================
# BYBIT API
# ==========================================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)



# ==========================================================
# ENV MODE
# ==========================================================

BYBIT_TESTNET = (
    os.getenv(
        "BYBIT_TESTNET",
        "true"
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



# ==========================================================
# ACCOUNT
# ==========================================================

# Bybit Unified Account
ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
)



# ==========================================================
# SYMBOL
# ==========================================================

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



CATEGORY = "linear"



# ==========================================================
# REST API
# ==========================================================

if BYBIT_TESTNET:

    BYBIT_BASE_URL = (
        "https://api-demo.bybit.com"
    )

else:

    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )



# ==========================================================
# WEBSOCKET
# ==========================================================

if BYBIT_TESTNET:


    BYBIT_PUBLIC_WS = (
        "wss://stream-demo.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream-demo.bybit.com/v5/private"
    )


else:


    BYBIT_PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream.bybit.com/v5/private"
    )



# ==========================================================
# TRADE SETTINGS
# ==========================================================


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



# ==========================================================
# RISK
# ==========================================================


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



# ==========================================================
# DEBUG
# ==========================================================

DEBUG = True



print("==============================")
print("[CONFIG LOADED]")
print("TESTNET :", BYBIT_TESTNET)
print("LIVE :", LIVE_TRADING)
print("ACCOUNT :", ACCOUNT_TYPE)
print("SYMBOL :", DEFAULT_SYMBOL)
print("BASE :", BYBIT_BASE_URL)
print("==============================")
