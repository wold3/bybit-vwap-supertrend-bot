# =====================================================
# config.py
# VWAP SUPERTREND AUTO BOT CONFIG
# =====================================================

import os

from dotenv import load_dotenv


load_dotenv()



# =====================================================
# MODE
# =====================================================

DEFAULT_MODE = os.getenv(

    "DEFAULT_MODE",

    "DEMO"

).upper()



LIVE = (

    DEFAULT_MODE == "LIVE"

)





# =====================================================
# API
# =====================================================

DEMO_API_KEY = os.getenv(

    "DEMO_API_KEY",

    ""

)


DEMO_API_SECRET = os.getenv(

    "DEMO_API_SECRET",

    ""

)




LIVE_API_KEY = os.getenv(

    "LIVE_API_KEY",

    ""

)


LIVE_API_SECRET = os.getenv(

    "LIVE_API_SECRET",

    ""

)




# 초기 호환용

if LIVE:


    BYBIT_API_KEY = LIVE_API_KEY

    BYBIT_API_SECRET = LIVE_API_SECRET


else:


    BYBIT_API_KEY = DEMO_API_KEY

    BYBIT_API_SECRET = DEMO_API_SECRET





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



# Bybit API 호환명

DEFAULT_SYMBOL = SYMBOL





# =====================================================
# LEVERAGE
# =====================================================

LEVERAGE = int(

    os.getenv(

        "LEVERAGE",

        "3"

    )

)





# =====================================================
# POSITION
# =====================================================

MAX_POSITION_SIZE = float(

    os.getenv(

        "MAX_POSITION_SIZE",

        "0.001"

    )

)


MAX_OPEN_POSITION = int(

    os.getenv(

        "MAX_OPEN_POSITION",

        "1"

    )

)





# =====================================================
# RISK
# =====================================================

RISK_PERCENT = float(

    os.getenv(

        "RISK_PERCENT",

        "1"

    )

)


STOP_LOSS_PERCENT = float(

    os.getenv(

        "STOP_LOSS_PERCENT",

        "1.5"

    )

)


TAKE_PROFIT_PERCENT = float(

    os.getenv(

        "TAKE_PROFIT_PERCENT",

        "3"

    )

)


TRAILING_STOP_PERCENT = float(

    os.getenv(

        "TRAILING_STOP_PERCENT",

        "1"

    )

)





# =====================================================
# VWAP
# =====================================================

VWAP_LENGTH = int(

    os.getenv(

        "VWAP_LENGTH",

        "20"

    )

)





# =====================================================
# SUPERTREND
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





# =====================================================
# CANDLE
# =====================================================

CANDLE_INTERVAL = os.getenv(

    "CANDLE_INTERVAL",

    "5"

)


MAX_HISTORY = int(

    os.getenv(

        "MAX_HISTORY",

        "500"

    )

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
# DATABASE
# =====================================================

DATABASE = os.getenv(

    "DATABASE",

    "bot.db"

)





# =====================================================
# WEB
# =====================================================

WEB_HOST = os.getenv(

    "WEB_HOST",

    "0.0.0.0"

)


WEB_PORT = int(

    os.getenv(

        "WEB_PORT",

        "8000"

    )

)





# =====================================================
# LOG
# =====================================================

LOG_LEVEL = os.getenv(

    "LOG_LEVEL",

    "INFO"

)





# =====================================================
# API RETRY
# =====================================================

API_TIMEOUT = int(

    os.getenv(

        "API_TIMEOUT",

        "10"

    )

)


API_RETRY = int(

    os.getenv(

        "API_RETRY",

        "3"

    )

)





# =====================================================
# PRINT
# =====================================================

print("=" * 30)

print(

    "[CONFIG LOADED]"

)

print("=" * 30)


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


print("=" * 30)
