# =====================================================
# config.py
# Global Configuration
# =====================================================

import os



# =====================================================
# BYBIT API
# =====================================================

# 우선순위:
# 1. Windows 환경변수
# 2. 직접 입력값


BYBIT_API_KEY = (

    os.getenv(
        "BYBIT_API_KEY"
    )

    or

    "sLo3fcWX9C7aGD2P0j"

)



BYBIT_API_SECRET = (

    os.getenv(
        "BYBIT_API_SECRET"
    )

    or

    "D0rel1YGg7ORgGr0DXW6p0XbLfiQBgdiP2Vy"

)





# =====================================================
# TRADING MODE
# =====================================================


# False = 테스트 주문
# True  = 실제 주문


LIVE = False







# =====================================================
# MARKET
# =====================================================


CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"


INTERVAL = "5"




LEVERAGE = 3







# =====================================================
# RISK MANAGEMENT
# =====================================================


RISK_PER_TRADE_PERCENT = 0.5


STOP_LOSS_PERCENT = 1.0


TAKE_PROFIT_PERCENT = 2.0



MAX_POSITION_SIZE = 1.0







# =====================================================
# INDICATOR
# =====================================================


ATR_PERIOD = 10


SUPERTREND_MULTIPLIER = 3



VWAP_PERIOD = 0



VOLUME_PERIOD = 20


MIN_VOLUME_MULTIPLIER = 1.2


USE_VOLUME_FILTER = True







# =====================================================
# ORDER
# =====================================================


ORDER_TYPE = "Market"


TIME_IN_FORCE = "IOC"




DEFAULT_ORDER_QTY = 0.001







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
# WEB SERVER
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
# CONFIG CHECK
# =====================================================


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


print(
    "API KEY LENGTH :",
    len(BYBIT_API_KEY)
)


print(
    "SECRET LENGTH :",
    len(BYBIT_API_SECRET)
)


print("==============================")





if BYBIT_API_KEY == "YOUR_API_KEY":


    print(
        "[WARNING] BYBIT API KEY NOT SET"
    )



if BYBIT_API_SECRET == "YOUR_API_SECRET":


    print(
        "[WARNING] BYBIT API SECRET NOT SET"
    )
