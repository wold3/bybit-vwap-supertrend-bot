# =====================================================
# config.py
# Bybit VWAP SuperTrend Bot Configuration
# =====================================================


import os



# =====================================================
# BOT MODE
# =====================================================


LIVE = False


TESTNET = False




# =====================================================
# BYBIT
# =====================================================


BYBIT_API_KEY = os.getenv(

    "BYBIT_API_KEY",

    ""

)


BYBIT_API_SECRET = os.getenv(

    "BYBIT_API_SECRET",

    ""

)



BYBIT_BASE_URL = (

    "https://api.bybit.com"

)



BYBIT_PRIVATE_WS = (

    "wss://stream.bybit.com/v5/private"

)







# =====================================================
# MARKET
# =====================================================


CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"


TIMEFRAME = "60"







# =====================================================
# LEVERAGE
# =====================================================


LEVERAGE = 3







# =====================================================
# RISK MANAGEMENT
# =====================================================


RISK_PER_TRADE_PERCENT = 0.5



STOP_LOSS_PERCENT = 1.5



TAKE_PROFIT_PERCENT = 3.0



MAX_POSITION_SIZE = 0.01







# =====================================================
# INDICATORS
# =====================================================


ATR_PERIOD = 14



SUPERTREND_MULTIPLIER = 3



VWAP_PERIOD = 0







# =====================================================
# VOLUME FILTER
# =====================================================


USE_VOLUME_FILTER = True



MIN_VOLUME_MULTIPLIER = 1.1







# =====================================================
# WATCHDOG
# =====================================================


WATCHDOG_INTERVAL = 10



MAX_API_ERROR = 5







# =====================================================
# TELEGRAM
# =====================================================


TELEGRAM_ENABLED = False



TELEGRAM_TOKEN = ""



TELEGRAM_CHAT_ID = ""







# =====================================================
# DATABASE
# =====================================================


DATABASE_FILE = (

    "database/trading.db"

)







# =====================================================
# ORDER SETTINGS
# =====================================================


ORDER_TYPE = "Market"



POSITION_MODE = "OneWay"







print("==============================")

print("[CONFIG LOADED]")

print(

    "LIVE :",


    LIVE

)


print(

    "CATEGORY :",


    CATEGORY

)


print(

    "SYMBOL :",


    DEFAULT_SYMBOL

)


print(

    "LEVERAGE :",


    LEVERAGE

)


print("==============================")
