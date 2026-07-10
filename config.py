# config.py


import os


# ==================================================
# BYBIT API
# ==================================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)



# True  = Testnet
# False = Real Trading

BYBIT_TESTNET = True



# Demo Trading Account

BYBIT_DEMO = False



# API URL 표시용

BYBIT_BASE_URL = (

    "https://api-testnet.bybit.com"

    if BYBIT_TESTNET

    else

    "https://api.bybit.com"

)



# ==================================================
# ACCOUNT
# ==================================================

ACCOUNT_TYPE = "UNIFIED"



CATEGORY = "linear"



DEFAULT_SYMBOL = "BTCUSDT"



# ==================================================
# ORDER
# ==================================================

ORDER_TYPE = "Market"



TIME_IN_FORCE = "IOC"



DEFAULT_QTY = 0.001



LEVERAGE = 5




# ==================================================
# POSITION
# ==================================================

MAX_POSITION_SIZE = 0.01



# One Way Mode

POSITION_MODE = "ONE_WAY"




# ==================================================
# RISK MANAGEMENT
# ==================================================

# 하루 최대 손실 %

MAX_DAILY_LOSS_PERCENT = 5



# 최대 전체 Drawdown %

MAX_DRAWDOWN_PERCENT = 15



# 한번 거래 위험 %

RISK_PER_TRADE_PERCENT = 1



# 최대 동시 포지션

MAX_OPEN_POSITION = 1



# 연속 손실 제한

MAX_LOSS_STREAK = 5



# 주문 쿨다운 초

ORDER_COOLDOWN = 60




# ==================================================
# STRATEGY
# ==================================================


# SuperTrend

ST_LENGTH = 14


ST_MULTIPLIER = 3.0



# ATR

ATR_PERIOD = 14



# VWAP

VWAP_ENABLED = True




# ==================================================
# TP / SL
# ==================================================


# 기본값

TAKE_PROFIT_PERCENT = 2.0


STOP_LOSS_PERCENT = 1.0



# ATR 기반 사용

USE_ATR_STOP = True


ATR_STOP_MULTIPLIER = 2.0


ATR_TP_MULTIPLIER = 3.0




# Trailing Stop

USE_TRAILING_STOP = True


TRAILING_PERCENT = 0.5




# ==================================================
# MARKET FILTER
# ==================================================


# 거래량 필터

USE_VOLUME_FILTER = True



MIN_VOLUME_MULTIPLIER = 1.2



# 변동성 필터

USE_VOLATILITY_FILTER = True



MAX_ATR_MULTIPLIER = 3




# ==================================================
# WEBSOCKET
# ==================================================

WS_RECONNECT_DELAY = 5


WS_HEARTBEAT = 30




# ==================================================
# WATCHDOG
# ==================================================

WATCHDOG_INTERVAL = 30



MAX_API_ERROR = 5




# ==================================================
# DATABASE
# ==================================================

DATABASE_PATH = "bot.db"




# ==================================================
# TELEGRAM
# ==================================================

TELEGRAM_TOKEN = os.getenv(

    "TELEGRAM_TOKEN",

    ""

)



TELEGRAM_CHAT_ID = os.getenv(

    "TELEGRAM_CHAT_ID",

    ""

)




# ==================================================
# LOGGING
# ==================================================

LOG_LEVEL = "INFO"


LOG_FILE = "bot.log"




# ==================================================
# SYSTEM
# ==================================================

DEBUG = True



TIMEZONE = "UTC"
