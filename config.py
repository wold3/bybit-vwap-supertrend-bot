# =====================================================
# config.py
# Global Configuration
# =====================================================


import os





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





# True = Real Trading
# False = Test Order

LIVE = False






CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"


INTERVAL = "5"




LEVERAGE = 3







# =====================================================
# RISK MANAGEMENT
# =====================================================


RISK_PER_TRADE_PERCENT = 0.5


STOP_LOSS_PERCENT = 1.0


MAX_POSITION_SIZE = 1.0







# =====================================================
# INDICATOR
# =====================================================


ATR_PERIOD = 10


SUPERTREND_MULTIPLIER = 3





VOLUME_PERIOD = 20


MIN_VOLUME_MULTIPLIER = 1.2


USE_VOLUME_FILTER = True







# =====================================================
# ORDER
# =====================================================


ORDER_TYPE = "Market"


TIME_IN_FORCE = "IOC"








# =====================================================
# DATABASE
# =====================================================


DATABASE_FILE = (

    "database/trading.db"

)








# =====================================================
# TELEGRAM
# =====================================================


TELEGRAM_ENABLED = False


TELEGRAM_TOKEN = ""


TELEGRAM_CHAT_ID = ""








# =====================================================
# WEBSERVER
# =====================================================


WEB_HOST = "0.0.0.0"


WEB_PORT = 8000








# =====================================================
# SYSTEM
# =====================================================


DEBUG = True


BOT_NAME = (

    "VWAP-SUPERTREND-BOT"

)








print("==============================")

print("[CONFIG LOADED]")

print("LIVE :", LIVE)

print("CATEGORY :", CATEGORY)

print("SYMBOL :", DEFAULT_SYMBOL)

print("LEVERAGE :", LEVERAGE)

print("==============================")
