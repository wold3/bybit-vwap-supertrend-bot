# =====================================================
# config.py
# VWAP SUPERTREND AUTO BOT CONFIG
# =====================================================

import os

from dotenv import load_dotenv


load_dotenv()





print("==============================")
print("[CONFIG LOADED]")
print("==============================")





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
# 기본 실행 모드
# DEMO : 모의투자
# LIVE : 실거래
#
# Dashboard에서 변경 가능

DEFAULT_MODE = "DEMO"


LIVE = False







# =====================================================
# MARKET
# =====================================================

CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"


INTERVAL = "5"





# =====================================================
# LEVERAGE
# =====================================================

LEVERAGE = 3





# =====================================================
# RISK MANAGEMENT
# =====================================================

# 1회 거래 위험률 (%)

RISK_PER_TRADE_PERCENT = 0.5



# 손절 %

STOP_LOSS_PERCENT = 1.0



# 익절 %

TAKE_PROFIT_PERCENT = 2.0



# 최대 주문 수량

MAX_POSITION_SIZE = 0.001





# =====================================================
# STRATEGY
# =====================================================

# ATR

ATR_PERIOD = 14



# SuperTrend 배수

SUPERTREND_MULTIPLIER = 3





# 거래량 필터

USE_VOLUME_FILTER = True


VOLUME_PERIOD = 20


MIN_VOLUME_MULTIPLIER = 1.2





# =====================================================
# DATABASE
# =====================================================

DATABASE_PATH = (

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

TELEGRAM_TOKEN = os.getenv(

    "TELEGRAM_TOKEN",

    ""

)


TELEGRAM_CHAT_ID = os.getenv(

    "TELEGRAM_CHAT_ID",

    ""

)





# =====================================================
# BOT CONTROL
# =====================================================

# 직접 실행 방식

AUTO_START = True



# 작업 스케줄러 사용 안 함

USE_TASK_SCHEDULER = False





# =====================================================
# DEBUG
# =====================================================

DEBUG = True







# =====================================================
# CONFIG CHECK
# =====================================================

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
