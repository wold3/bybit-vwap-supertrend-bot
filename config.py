# =====================================================
# config.py
# VWAP SUPERTREND BOT CONFIG
# =====================================================


import os



# =====================================================
# MODE
# =====================================================

# DEMO : 모의투자
# LIVE : 실거래

DEFAULT_MODE = "DEMO"



LIVE = False






# =====================================================
# BYBIT API
# =====================================================

BYBIT_API_KEY = os.getenv(

    "BYBIT_API_KEY",

    "YOUR_API_KEY"

)


BYBIT_API_SECRET = os.getenv(

    "BYBIT_API_SECRET",

    "YOUR_API_SECRET"

)







# =====================================================
# MARKET
# =====================================================

CATEGORY = "linear"


SYMBOL = "BTCUSDT"


SETTLE_COIN = "USDT"





# =====================================================
# TRADE
# =====================================================

LEVERAGE = 3



POSITION_MODE = "ONE_WAY"



MARGIN_TYPE = "ISOLATED"








# =====================================================
# ORDER
# =====================================================

# BTCUSDT 최소 주문 단위에 맞게 조정

MAX_POSITION_SIZE = 0.001



ORDER_COOLDOWN = 30






# =====================================================
# TAKE PROFIT / STOP LOSS
# =====================================================

TAKE_PROFIT_PERCENT = 1.0



STOP_LOSS_PERCENT = 0.5







# =====================================================
# RISK MANAGEMENT
# =====================================================

RISK_PER_TRADE_PERCENT = 1.0



MAX_DAILY_LOSS_PERCENT = 5.0



MAX_LOSS_COUNT = 5






# =====================================================
# STRATEGY
# =====================================================

TIMEFRAME = "5"



ATR_PERIOD = 10



SUPERTREND_MULTIPLIER = 3






# =====================================================
# MARKET LOOP
# =====================================================

CANDLE_LIMIT = 200



LOOP_INTERVAL = 10






# =====================================================
# TELEGRAM
# =====================================================

TELEGRAM_ENABLE = False



TELEGRAM_TOKEN = ""



TELEGRAM_CHAT_ID = ""








# =====================================================
# DATABASE
# =====================================================

DATABASE_FILE = "bot.db"







# =====================================================
# WEB
# =====================================================

WEB_HOST = "0.0.0.0"


WEB_PORT = 8000







# =====================================================
# DEBUG
# =====================================================

DEBUG = False






print("==============================")

print("[CONFIG LOADED]")

print("==============================")

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

print("==============================")
