# =====================================================
# config.py
# BYBIT VWAP SUPERTREND BOT CONFIG
# =====================================================

import os



print("==============================")
print("[CONFIG LOADED]")
print()



# =====================================================
# MODE
# =====================================================

LIVE = False


# True  = 실제 주문
# False = 테스트용


CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"


ACCOUNT_TYPE = "UNIFIED"





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



BYBIT_REST_URL = (

    "https://api.bybit.com"

)


BYBIT_PRIVATE_WS = (

    "wss://stream.bybit.com/v5/private"

)







# =====================================================
# LEVERAGE
# =====================================================

LEVERAGE = 3






# =====================================================
# ORDER
# =====================================================

DEFAULT_QTY = 0.001


ORDER_COOLDOWN = 60



MAX_POSITION_SIZE = 0.01







# =====================================================
# RISK MANAGEMENT
# =====================================================

RISK_PER_TRADE_PERCENT = 1.0



MAX_DAILY_LOSS_PERCENT = 5



MAX_DRAWDOWN_PERCENT = 10



MAX_LOSS_STREAK = 3







# =====================================================
# STOP / TAKE PROFIT
# =====================================================

STOP_LOSS_PERCENT = 1.5


TAKE_PROFIT_PERCENT = 3.0







# =====================================================
# INDICATOR
# =====================================================

ATR_PERIOD = 14



SUPERTREND_MULTIPLIER = 3



VWAP_PERIOD = 20







# =====================================================
# VOLUME FILTER
# =====================================================

USE_VOLUME_FILTER = False



MIN_VOLUME_MULTIPLIER = 0.8







# =====================================================
# WATCHDOG
# =====================================================

WATCHDOG_INTERVAL = 30


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

    "trading.db"

)







# =====================================================
# PRINT
# =====================================================

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
