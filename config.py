# =====================================================
# config.py
# Bybit VWAP SuperTrend Bot Configuration
# =====================================================

import os
from dotenv import load_dotenv


load_dotenv()





# =====================================================
# ENV
# =====================================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)



TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
)


TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)







# =====================================================
# MODE
# =====================================================

LIVE = os.getenv(
    "LIVE",
    "False"
).lower() == "true"



DEMO = os.getenv(
    "DEMO",
    "True"
).lower() == "true"



TESTNET = os.getenv(
    "TESTNET",
    "False"
).lower() == "true"







# =====================================================
# BYBIT
# =====================================================

ACCOUNT_TYPE = "UNIFIED"



CATEGORY = os.getenv(

    "CATEGORY",

    "linear"

)



DEFAULT_SYMBOL = os.getenv(

    "SYMBOL",

    "BTCUSDT"

)



SYMBOL = DEFAULT_SYMBOL





# REST URL

if TESTNET:


    BYBIT_REST_URL = (

        "https://api-testnet.bybit.com"

    )


else:


    if DEMO:


        BYBIT_REST_URL = (

            "https://api-demo.bybit.com"

        )

    else:


        BYBIT_REST_URL = (

            "https://api.bybit.com"

        )







# PRIVATE WS

if TESTNET:


    BYBIT_PRIVATE_WS = (

        "wss://stream-testnet.bybit.com/v5/private"

    )


else:


    if DEMO:


        BYBIT_PRIVATE_WS = (

            "wss://stream-demo.bybit.com/v5/private"

        )


    else:


        BYBIT_PRIVATE_WS = (

            "wss://stream.bybit.com/v5/private"

        )







# =====================================================
# TRADING
# =====================================================

DEFAULT_QTY = float(

    os.getenv(

        "DEFAULT_QTY",

        "0.001"

    )

)



LEVERAGE = int(

    os.getenv(

        "LEVERAGE",

        "3"

    )

)







# =====================================================
# RISK MANAGEMENT
# =====================================================

RISK_PER_TRADE_PERCENT = float(

    os.getenv(

        "RISK_PER_TRADE_PERCENT",

        "1"

    )

)



MAX_POSITION_SIZE = float(

    os.getenv(

        "MAX_POSITION_SIZE",

        "0.05"

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

        "10"

    )

)



MAX_LOSS_STREAK = int(

    os.getenv(

        "MAX_LOSS_STREAK",

        "5"

    )

)



ORDER_COOLDOWN = int(

    os.getenv(

        "ORDER_COOLDOWN",

        "300"

    )

)







# =====================================================
# STOP LOSS / TAKE PROFIT
# =====================================================

STOP_LOSS_PERCENT = float(

    os.getenv(

        "STOP_LOSS_PERCENT",

        "1"

    )

)



TAKE_PROFIT_PERCENT = float(

    os.getenv(

        "TAKE_PROFIT_PERCENT",

        "2"

    )

)







# =====================================================
# INDICATORS
# =====================================================

ATR_PERIOD = int(

    os.getenv(

        "ATR_PERIOD",

        "14"

    )

)



SUPERTREND_MULTIPLIER = float(

    os.getenv(

        "SUPERTREND_MULTIPLIER",

        "3"

    )

)



VWAP_PERIOD = int(

    os.getenv(

        "VWAP_PERIOD",

        "50"

    )

)







# =====================================================
# VOLUME FILTER
# =====================================================

USE_VOLUME_FILTER = (

    os.getenv(

        "USE_VOLUME_FILTER",

        "True"

    ).lower()

    ==

    "true"

)



MIN_VOLUME_MULTIPLIER = float(

    os.getenv(

        "MIN_VOLUME_MULTIPLIER",

        "1.2"

    )

)







# =====================================================
# WATCHDOG
# =====================================================

WATCHDOG_INTERVAL = int(

    os.getenv(

        "WATCHDOG_INTERVAL",

        "30"

    )

)



MAX_API_ERROR = int(

    os.getenv(

        "MAX_API_ERROR",

        "5"

    )

)







# =====================================================
# DATABASE
# =====================================================

DATABASE_PATH = os.getenv(

    "DATABASE_PATH",

    "data/trading.db"

)







# =====================================================
# OUTPUT
# =====================================================

print("==============================")
print("[CONFIG LOADED]")
print("LIVE :", LIVE)
print("DEMO :", DEMO)
print("TESTNET :", TESTNET)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")
