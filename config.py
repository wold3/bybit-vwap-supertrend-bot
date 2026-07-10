import os
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# MODE
# ==================================================

BYBIT_DEMO = True
BYBIT_TESTNET = False
LIVE = False

DEMO = BYBIT_DEMO

# ==================================================
# API
# ==================================================

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "")

# ==================================================
# ACCOUNT
# ==================================================

ACCOUNT = "UNIFIED"
ACCOUNT_TYPE = ACCOUNT

CATEGORY = "linear"

SYMBOL = "BTCUSDT"
DEFAULT_SYMBOL = SYMBOL

# ==================================================
# REST URL
# ==================================================

if BYBIT_DEMO:
    REST_URL = "https://api-demo.bybit.com"
elif BYBIT_TESTNET:
    REST_URL = "https://api-testnet.bybit.com"
else:
    REST_URL = "https://api.bybit.com"

BYBIT_BASE_URL = REST_URL

# ==================================================
# WEBSOCKET
# ==================================================

PUBLIC_WS = "wss://stream.bybit.com/v5/public"

if BYBIT_DEMO:
    PRIVATE_WS = "wss://stream-demo.bybit.com/v5/private"
elif BYBIT_TESTNET:
    PRIVATE_WS = "wss://stream-testnet.bybit.com/v5/private"
else:
    PRIVATE_WS = "wss://stream.bybit.com/v5/private"

# ==================================================
# ORDER
# ==================================================

QTY = 0.001
DEFAULT_QTY = QTY

LEVERAGE = 3

ORDER_TYPE = "Market"
TIME_IN_FORCE = "GTC"

ORDER_COOLDOWN = 60

# ==================================================
# STRATEGY
# ==================================================

VWAP_LENGTH = 20

SUPERTREND_PERIOD = 5
SUPERTREND_MULTIPLIER = 2.0

# ==================================================
# POSITION / EXIT
# ==================================================

TAKE_PROFIT_PERCENT = 1.0
STOP_LOSS_PERCENT = 0.5

# ==================================================
# RISK
# ==================================================

MAX_POSITION_SIZE = 0.01
MAX_DAILY_LOSS_PERCENT = 5.0

# ==================================================
# LOG
# ==================================================

print("==============================")
print("[CONFIG LOADED]")
print("DEMO :", DEMO)
print("BYBIT_DEMO :", BYBIT_DEMO)
print("TESTNET :", BYBIT_TESTNET)
print("LIVE :", LIVE)
print("ACCOUNT :", ACCOUNT_TYPE)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("QTY :", DEFAULT_QTY)
print("LEVERAGE :", LEVERAGE)
print("ORDER COOLDOWN :", ORDER_COOLDOWN)
print("VWAP :", VWAP_LENGTH)
print("SUPERTREND :", SUPERTREND_PERIOD, SUPERTREND_MULTIPLIER)
print("REST :", BYBIT_BASE_URL)
print("PUBLIC WS :", PUBLIC_WS)
print("PRIVATE WS :", PRIVATE_WS)
print("==============================")
