import os
from dotenv import load_dotenv


load_dotenv()



# ==================================================
# API KEY
# ==================================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)



# ==================================================
# MODE
# ==================================================

BYBIT_TESTNET = (

    os.getenv(
        "BYBIT_TESTNET",
        "false"
    )
    .lower()
    == "true"

)


BYBIT_DEMO = (

    os.getenv(
        "BYBIT_DEMO",
        "true"
    )
    .lower()
    == "true"

)


LIVE_TRADING = (

    os.getenv(
        "LIVE_TRADING",
        "false"
    )
    .lower()
    == "true"

)



# ==================================================
# REST URL
# ==================================================

if BYBIT_TESTNET:

    BYBIT_BASE_URL = (
        "https://api-testnet.bybit.com"
    )


elif BYBIT_DEMO:

    BYBIT_BASE_URL = (
        "https://api-demo.bybit.com"
    )


else:

    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )




# ==================================================
# WEBSOCKET
# ==================================================

if BYBIT_TESTNET:

    BYBIT_PUBLIC_WS = (
        "wss://stream-testnet.bybit.com/v5/public"
    )

    BYBIT_PRIVATE_WS = (
        "wss://stream-testnet.bybit.com/v5/private"
    )


elif BYBIT_DEMO:

    BYBIT_PUBLIC_WS = (
        "wss://stream-demo.bybit.com/v5/public"
    )

    BYBIT_PRIVATE_WS = (
        "wss://stream-demo.bybit.com/v5/private"
    )


else:

    BYBIT_PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public"
    )

    BYBIT_PRIVATE_WS = (
        "wss://stream.bybit.com/v5/private"
    )




# ==================================================
# ACCOUNT
# ==================================================

ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
)


CATEGORY = os.getenv(
    "CATEGORY",
    "linear"
)




# ==================================================
# SYMBOL
# ==================================================

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)




# ==================================================
# ORDER
# ==================================================

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



# ==================================================
# LEVERAGE
# ==================================================

LEVERAGE = int(
    os.getenv(
        "LEVERAGE",
        "3"
    )
)




# ==================================================
# RISK
# ==================================================

MAX_POSITION_SIZE = float(
    os.getenv(
        "MAX_POSITION_SIZE",
        "0.001"
    )
)


MAX_DAILY_LOSS_PERCENT = float(
    os.getenv(
        "MAX_DAILY_LOSS_PERCENT",
        "5"
    )
)




# ==================================================
# TP / SL
# ==================================================

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




# ==================================================
# INDICATOR
# ==================================================

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




# ==================================================
# LOG
# ==================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)




print("==============================")
print("[CONFIG LOADED]")
print("DEMO :", BYBIT_DEMO)
print("TESTNET :", BYBIT_TESTNET)
print("LIVE :", LIVE_TRADING)
print("ACCOUNT :", ACCOUNT_TYPE)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("QTY :", DEFAULT_QTY)
print("LEVERAGE :", LEVERAGE)
print("ORDER COOLDOWN :", ORDER_COOLDOWN)
print("VWAP :", VWAP_LENGTH)
print(
    "SUPERTREND :",
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER
)
print("REST :", BYBIT_BASE_URL)
print("PUBLIC WS :", BYBIT_PUBLIC_WS)
print("PRIVATE WS :", BYBIT_PRIVATE_WS)
print("==============================")
