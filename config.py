import os


# =====================================================
# ENVIRONMENT
# =====================================================

LIVE_TRADING = False


TESTNET = False


DEMO_TRADING = True





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
# ACCOUNT
# =====================================================

ACCOUNT_TYPE = "UNIFIED"





# =====================================================
# SYMBOL
# =====================================================

DEFAULT_SYMBOL = "BTCUSDT"





# =====================================================
# CATEGORY
# =====================================================

CATEGORY = "linear"





# =====================================================
# REST API
# =====================================================


if DEMO_TRADING:


    BYBIT_BASE_URL = (
        "https://api-demo.bybit.com"
    )


elif TESTNET:


    BYBIT_BASE_URL = (
        "https://api-testnet.bybit.com"
    )


else:


    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )







# =====================================================
# WEBSOCKET
# =====================================================


if DEMO_TRADING:


    BYBIT_PUBLIC_WS = (
        "wss://stream-demo.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream-demo.bybit.com/v5/private"
    )



elif TESTNET:


    BYBIT_PUBLIC_WS = (
        "wss://stream-testnet.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream-testnet.bybit.com/v5/private"
    )



else:


    BYBIT_PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream.bybit.com/v5/private"
    )









# =====================================================
# TRADING SETTINGS
# =====================================================


LEVERAGE = 5


DEFAULT_QTY = 0.001



TIMEFRAME = "1"





# =====================================================
# STRATEGY
# =====================================================


VWAP_LENGTH = 20


SUPERTREND_PERIOD = 10


SUPERTREND_MULTIPLIER = 3







# =====================================================
# RISK
# =====================================================


MAX_POSITION_SIZE = 0.01


DAILY_LOSS_LIMIT = -100


ORDER_COOLDOWN = 30







# =====================================================
# LOG
# =====================================================

LOG_LEVEL = "INFO"





print("==============================")
print("[CONFIG LOADED]")
print("DEMO :", DEMO_TRADING)
print("TESTNET :", TESTNET)
print("LIVE :", LIVE_TRADING)
print("ACCOUNT :", ACCOUNT_TYPE)
print("SYMBOL :", DEFAULT_SYMBOL)
print("BASE :", BYBIT_BASE_URL)
print("==============================")
