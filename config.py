# =====================================================
# config.py
# VWAP SUPERTREND BOT CONFIG
# Demo / Live Support
# =====================================================

import os

from dotenv import load_dotenv


load_dotenv()



print("==============================")
print("[CONFIG LOADED]")
print("==============================")





# =====================================================
# API KEY
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


# False = Bybit Demo Trading
# True  = Real Trading


LIVE = False





print(

    "LIVE :",

    LIVE

)









# =====================================================
# MARKET
# =====================================================


CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"


INTERVAL = "5"





print(

    "CATEGORY :",

    CATEGORY

)


print(

    "SYMBOL :",

    DEFAULT_SYMBOL

)









# =====================================================
# LEVERAGE
# =====================================================


LEVERAGE = 3



print(

    "LEVERAGE :",

    LEVERAGE

)









# =====================================================
# STRATEGY
# =====================================================


# SuperTrend

ATR_PERIOD = 10


SUPERTREND_MULTIPLIER = 3







# Volume Filter


USE_VOLUME_FILTER = True


VOLUME_PERIOD = 20


MIN_VOLUME_MULTIPLIER = 1.2







# =====================================================
# RISK MANAGEMENT
# =====================================================


# 거래당 위험 %

RISK_PER_TRADE_PERCENT = 0.5



# 손절 %

STOP_LOSS_PERCENT = 1.0



# 최대 주문 BTC 수량

MAX_POSITION_SIZE = 0.001







# =====================================================
# TAKE PROFIT
# =====================================================


TAKE_PROFIT_PERCENT = 2.0







# =====================================================
# DATABASE
# =====================================================


DATABASE_FILE = (

    "database/trading.db"

)









# =====================================================
# WEB DASHBOARD
# =====================================================


WEB_HOST = "0.0.0.0"


WEB_PORT = 8000







# =====================================================
# TELEGRAM
# =====================================================


TELEGRAM_ENABLE = False


TELEGRAM_TOKEN = os.getenv(

    "TELEGRAM_TOKEN",

    ""

)


TELEGRAM_CHAT_ID = os.getenv(

    "TELEGRAM_CHAT_ID",

    ""

)









# =====================================================
# SYSTEM
# =====================================================


BOT_NAME = (

    "VWAP_SUPERTREND_BOT"

)



VERSION = "1.0"





print(

    "API KEY LENGTH :",

    len(BYBIT_API_KEY)

)


print(

    "SECRET LENGTH :",

    len(BYBIT_API_SECRET)

)


print("==============================")
