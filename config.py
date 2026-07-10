# =====================================================
# config.py
# BOT GLOBAL CONFIG
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





# Demo Trading

BYBIT_REST_URL = os.getenv(

    "BYBIT_REST_URL",

    "https://api-demo.bybit.com"

)



BYBIT_PRIVATE_WS = os.getenv(

    "BYBIT_PRIVATE_WS",

    "wss://stream-demo.bybit.com/v5/private"

)







# =====================================================
# MARKET
# =====================================================


CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"


ACCOUNT_TYPE = "UNIFIED"







# =====================================================
# LEVERAGE
# =====================================================


LEVERAGE = int(

    os.getenv(

        "LEVERAGE",

        5

    )

)







# =====================================================
# ORDER
# =====================================================


DEFAULT_QTY = float(

    os.getenv(

        "DEFAULT_QTY",

        0.001

    )

)







# =====================================================
# RISK MANAGEMENT
# =====================================================


RISK_PER_TRADE_PERCENT = float(

    os.getenv(

        "RISK_PER_TRADE_PERCENT",

        1

    )

)



MAX_POSITION_SIZE = float(

    os.getenv(

        "MAX_POSITION_SIZE",

        0.01

    )

)



MAX_DAILY_LOSS_PERCENT = float(

    os.getenv(

        "MAX_DAILY_LOSS_PERCENT",

        5

    )

)



MAX_DRAWDOWN_PERCENT = float(

    os.getenv(

        "MAX_DRAWDOWN_PERCENT",

        10

    )

)



MAX_LOSS_STREAK = int(

    os.getenv(

        "MAX_LOSS_STREAK",

        3

    )

)



ORDER_COOLDOWN = int(

    os.getenv(

        "ORDER_COOLDOWN",

        300

    )

)







# =====================================================
# STOP / TAKE PROFIT
# =====================================================


STOP_LOSS_PERCENT = float(

    os.getenv(

        "STOP_LOSS_PERCENT",

        1

    )

)



TAKE_PROFIT_PERCENT = float(

    os.getenv(

        "TAKE_PROFIT_PERCENT",

        2

    )

)







# =====================================================
# INDICATOR
# =====================================================


ATR_PERIOD = int(

    os.getenv(

        "ATR_PERIOD",

        14

    )

)



SUPERTREND_MULTIPLIER = float(

    os.getenv(

        "SUPERTREND_MULTIPLIER",

        3

    )

)







# =====================================================
# VOLUME FILTER
# =====================================================


USE_VOLUME_FILTER = True



MIN_VOLUME_MULTIPLIER = float(

    os.getenv(

        "MIN_VOLUME_MULTIPLIER",

        1.2

    )

)







# =====================================================
# WATCHDOG
# =====================================================


WATCHDOG_INTERVAL = int(

    os.getenv(

        "WATCHDOG_INTERVAL",

        30

    )

)



MAX_API_ERROR = int(

    os.getenv(

        "MAX_API_ERROR",

        5

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







print("==============================")

print("[CONFIG LOADED]")

print("CATEGORY :", CATEGORY)

print("SYMBOL   :", DEFAULT_SYMBOL)

print("ACCOUNT  :", ACCOUNT_TYPE)

print("LEVERAGE :", LEVERAGE)

print("==============================")
