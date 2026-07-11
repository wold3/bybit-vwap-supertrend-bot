# =====================================================
# config.py
# VWAP SUPERTREND BOT CONFIGURATION
# =====================================================

import os

from dotenv import load_dotenv


load_dotenv()





# =====================================================
# BYBIT API
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
# TRADING MODE
# =====================================================

# 초기 실행 모드
# DEMO / LIVE

DEFAULT_MODE = os.getenv(
    "DEFAULT_MODE",
    "DEMO"
).upper()



LIVE = (

    DEFAULT_MODE == "LIVE"

)





# =====================================================
# MARKET
# =====================================================

CATEGORY = os.getenv(
    "CATEGORY",
    "linear"
)


SYMBOL = os.getenv(
    "SYMBOL",
    "BTCUSDT"
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
        "0.5"
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



MAX_POSITION_SIZE = float(

    os.getenv(
        "MAX_POSITION_SIZE",
        "0.001"
    )

)





# =====================================================
# STRATEGY
# =====================================================

ATR_PERIOD = int(

    os.getenv(
        "ATR_PERIOD",
        "10"
    )

)



SUPERTREND_MULTIPLIER = float(

    os.getenv(
        "SUPERTREND_MULTIPLIER",
        "3"
    )

)





USE_VOLUME_FILTER = (

    os.getenv(
        "USE_VOLUME_FILTER",
        "True"
    ).lower()

    ==

    "true"

)



VOLUME_PERIOD = int(

    os.getenv(
        "VOLUME_PERIOD",
        "20"
    )

)



MIN_VOLUME_MULTIPLIER = float(

    os.getenv(
        "MIN_VOLUME_MULTIPLIER",
        "1.2"
    )

)





# =====================================================
# DATABASE
# =====================================================

DB_FILE = os.getenv(

    "DB_FILE",

    "bot.db"

)





# =====================================================
# TELEGRAM
# =====================================================

TELEGRAM_TOKEN = os.getenv(

    "TELEGRAM_TOKEN",

    ""

)


TELEGRAM_CHAT_ID = os.getenv(

    "TELEGRAM_CHAT_ID",

    ""

)





# =====================================================
# WEB
# =====================================================

WEB_PORT = int(

    os.getenv(
        "WEB_PORT",
        "8000"
    )

)





# =====================================================
# PRINT CONFIG
# =====================================================

print(
    "=============================="
)

print(
    "[CONFIG LOADED]"
)

print(
    "=============================="
)

print(
    "LIVE :",
    LIVE
)

print(
    "DEFAULT MODE :",
    DEFAULT_MODE
)

print(
    "CATEGORY :",
    CATEGORY
)

print(
    "SYMBOL :",
    SYMBOL
)

print(
    "LEVERAGE :",
    LEVERAGE
)

print(
    "API KEY LENGTH :",
    len(BYBIT_API_KEY)
)

print(
    "SECRET LENGTH :",
    len(BYBIT_API_SECRET)
)

print(
    "=============================="
)
