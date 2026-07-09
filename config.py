import os
from dotenv import load_dotenv


# ==========================================================
# ENV LOAD
# ==========================================================

load_dotenv()



# ==========================================================
# BYBIT MODE
# ==========================================================

BYBIT_TESTNET = (
    os.getenv(
        "BYBIT_TESTNET",
        "False"
    ).lower()
    == "true"
)



# Demo Trading 사용 여부
BYBIT_DEMO = (
    os.getenv(
        "BYBIT_DEMO",
        "True"
    ).lower()
    == "true"
)



# ==========================================================
# API KEY
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
# REST URL
# ==========================================================

if BYBIT_DEMO:


    BYBIT_BASE_URL = (
        "https://api-demo.bybit.com"
    )


elif BYBIT_TESTNET:


    BYBIT_BASE_URL = (
        "https://api-testnet.bybit.com"
    )


else:


    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )





# ==========================================================
# WEBSOCKET URL
# ==========================================================


if BYBIT_DEMO:


    BYBIT_PUBLIC_WS = (
        "wss://stream-demo.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream-demo.bybit.com/v5/private"
    )



elif BYBIT_TESTNET:


    BYBIT_PUBLIC_WS = (
        "wss://stream-testnet.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream-testnet.bybit.com/v5/private"
    )



else:


    BYBIT_PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream.bybit.com/v5/private"
    )





# ==========================================================
# TRADING CONFIG
# ==========================================================


DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



LIVE_TRADING = (
    os.getenv(
        "LIVE_TRADING",
        "False"
    ).lower()
    == "true"
)



DEFAULT_QTY = float(
    os.getenv(
        "DEFAULT_QTY",
        "0.001"
    )
)




# ==========================================================
# STRATEGY CONFIG
# ==========================================================


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




# ==========================================================
# RISK CONFIG
# ==========================================================


MAX_POSITION_SIZE = float(
    os.getenv(
        "MAX_POSITION_SIZE",
        "0.01"
    )
)



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
# LOG
# ==========================================================


print("==============================")
print("[CONFIG LOADED]")
print("DEMO :", BYBIT_DEMO)
print("TESTNET :", BYBIT_TESTNET)
print("LIVE :", LIVE_TRADING)
print("BASE :", BYBIT_BASE_URL)
print("PUBLIC WS :", BYBIT_PUBLIC_WS)
print("PRIVATE WS :", BYBIT_PRIVATE_WS)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")
