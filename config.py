import os
from dotenv import load_dotenv


load_dotenv()



# ==========================================
# MODE
# ==========================================

# Bybit Demo Trading
BYBIT_DEMO = True

# Testnet 여부
BYBIT_TESTNET = False

# Live Trading
LIVE = False


# 기존 코드 호환용
DEMO = BYBIT_DEMO





# ==========================================
# API KEY
# ==========================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)





# ==========================================
# ACCOUNT
# ==========================================

ACCOUNT = "UNIFIED"


CATEGORY = "linear"


DEFAULT_SYMBOL = "BTCUSDT"

SYMBOL = DEFAULT_SYMBOL





# ==========================================
# REST API
# ==========================================

if BYBIT_DEMO:

    REST_URL = "https://api-demo.bybit.com"

elif BYBIT_TESTNET:

    REST_URL = "https://api-testnet.bybit.com"

else:

    REST_URL = "https://api.bybit.com"





# ==========================================
# WEBSOCKET
# ==========================================

# Market Data
# Demo 계정도 일반 Public WS 사용

PUBLIC_WS = (
    "wss://stream.bybit.com/v5/public"
)



# Account Private WS
PRIVATE_WS = (
    "wss://stream-demo.bybit.com/v5/private"
    if BYBIT_DEMO
    else "wss://stream.bybit.com/v5/private"
)





# ==========================================
# TRADE SETTINGS
# ==========================================

QTY = 0.001


LEVERAGE = 3


ORDER_COOLDOWN = 60





# ==========================================
# INDICATOR SETTINGS
# ==========================================

VWAP_LENGTH = 20


SUPERTREND_PERIOD = 5


SUPERTREND_MULTIPLIER = 2.0





# 기존 출력 호환

VWAP = VWAP_LENGTH


SUPERTREND = (
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER
)





# ==========================================
# RISK MANAGEMENT
# ==========================================

MAX_DAILY_LOSS_PERCENT = 5.0





# ==========================================
# DEBUG
# ==========================================

print("==============================")
print("[CONFIG LOADED]")
print("DEMO :", DEMO)
print("BYBIT_DEMO :", BYBIT_DEMO)
print("TESTNET :", BYBIT_TESTNET)
print("LIVE :", LIVE)
print("ACCOUNT :", ACCOUNT)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", SYMBOL)
print("QTY :", QTY)
print("LEVERAGE :", LEVERAGE)
print("ORDER COOLDOWN :", ORDER_COOLDOWN)
print("VWAP :", VWAP_LENGTH)
print(
    "SUPERTREND :",
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER
)
print("REST :", REST_URL)
print("PUBLIC WS :", PUBLIC_WS)
print("PRIVATE WS :", PRIVATE_WS)
print("==============================")
