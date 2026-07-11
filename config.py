# =====================================================
# config.py
# Global Configuration
# =====================================================

import os



# =====================================================
# TRADING MODE
# =====================================================

# demo : Bybit Demo Trading
# test : Bybit Testnet
# live : Real Trading

TRADING_MODE = "demo"





# =====================================================
# BYBIT API KEY
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
# BYBIT ENDPOINT
# =====================================================


if TRADING_MODE == "demo":


    BYBIT_BASE_URL = (
        "https://api-demo.bybit.com"
    )


    BYBIT_WS_URL = (
        "wss://stream-demo.bybit.com"
    )



elif TRADING_MODE == "live":


    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )


    BYBIT_WS_URL = (
        "wss://stream.bybit.com"
    )



else:


    BYBIT_BASE_URL = (
        "https://api-testnet.bybit.com"
    )


    BYBIT_WS_URL = (
        "wss://stream-testnet.bybit.com"
    )







# =====================================================
# MARKET
# =====================================================

CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"


INTERVAL = "5"




LEVERAGE = 3







# =====================================================
# ORDER
# =====================================================


# True:
# Bybit 주문 실행
#
# False:
# 내부 테스트 주문

LIVE_ORDER = True



DEFAULT_ORDER_QTY = 0.001


ORDER_TYPE = "Market"


TIME_IN_FORCE = "IOC"







# =====================================================
# MANUAL TEST ORDER
# =====================================================


# Demo Trading 주문 테스트용

MANUAL_TEST_ORDER = False


TEST_ORDER_SIDE = "Buy"








# =====================================================
# RISK MANAGEMENT
# =====================================================


RISK_PER_TRADE_PERCENT = 0.5


MAX_POSITION_SIZE = 1.0



STOP_LOSS_PERCENT = 1.0


TAKE_PROFIT_PERCENT = 2.0



MAX_DAILY_LOSS_PERCENT = 3.0







# =====================================================
# INDICATOR
# =====================================================


ATR_PERIOD = 10


SUPERTREND_MULTIPLIER = 3



VOLUME_PERIOD = 20


MIN_VOLUME_MULTIPLIER = 1.2


USE_VOLUME_FILTER = True







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
# WEB DASHBOARD
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







# =====================================================
# START LOG
# =====================================================


print("==============================")

print("[CONFIG LOADED]")

print(
    "MODE :",
    TRADING_MODE
)

print(
    "BASE :",
    BYBIT_BASE_URL
)

print(
    "SYMBOL :",
    DEFAULT_SYMBOL
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
