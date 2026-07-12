# =====================================================
# config.py
# VWAP SUPERTREND BOT V3
# GLOBAL CONFIGURATION
# =====================================================


# =====================================================
# BYBIT MODE
# =====================================================


MODE = "DEMO"


# DEMO API

DEMO_API_KEY = "YOUR_DEMO_API_KEY"

DEMO_API_SECRET = "YOUR_DEMO_API_SECRET"



# LIVE API

LIVE_API_KEY = "YOUR_LIVE_API_KEY"

LIVE_API_SECRET = "YOUR_LIVE_API_SECRET"







# =====================================================
# BYBIT SETTINGS
# =====================================================


CATEGORY = "linear"


SYMBOL = "BTCUSDT"



# 레버리지

LEVERAGE = 100


MAX_LEVERAGE = 100







# =====================================================
# ACCOUNT
# =====================================================


# 기본 투자금

CAPITAL = 1000



# 최대 포지션

MAX_POSITION_SIZE = 0.001



# 최대 동시 포지션

MAX_OPEN_POSITION = 1



# 하루 최대 손실

MAX_DAILY_LOSS = 50







# =====================================================
# STRATEGY
# =====================================================


# VWAP

VWAP_LENGTH = 50



# ATR

ATR_PERIOD = 10



# SuperTrend 배수

SUPERTREND_MULTIPLIER = 3







# =====================================================
# TIMEFRAME
# =====================================================


TIMEFRAME = "5"




# =====================================================
# AUTO TP / SL
# =====================================================


# 기본 TP

TAKE_PROFIT_PERCENT = 5



# 기본 SL

STOP_LOSS_PERCENT = 2







# =====================================================
# SPLIT TAKE PROFIT
# =====================================================


# 1차 익절

TP1_PERCENT = 3


# 2차 익절

TP2_PERCENT = 7


# 3차 익절

TP3_PERCENT = 15





# 익절 비율

TP1_SIZE = 30


TP2_SIZE = 40


TP3_SIZE = 30







# =====================================================
# SPLIT ENTRY
# =====================================================


# 1차 진입

ENTRY1_PERCENT = 60



# 2차 추가진입

ENTRY2_PERCENT = 40







# =====================================================
# ORDER
# =====================================================


ORDER_TYPE = "Market"



# 주문 재시도

ORDER_RETRY = 3



# 주문 대기시간

ORDER_COOLDOWN = 3







# =====================================================
# SYSTEM
# =====================================================


LOG_LIMIT = 300



UPDATE_INTERVAL = 2




# =====================================================
# SYMBOL LIST
# =====================================================


AVAILABLE_SYMBOLS = [

    "BTCUSDT",

    "ETHUSDT",

    "SOLUSDT",

    "XRPUSDT"

]





print(

    "[CONFIG LOADED]",

    MODE,

    SYMBOL,

    f"{LEVERAGE}X"

)
