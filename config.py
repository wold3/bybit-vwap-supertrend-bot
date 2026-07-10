# ==================================================
# CONFIGURATION
# ==================================================

import os

from dotenv import load_dotenv


load_dotenv()



# ==================================================
# TYPE CONVERTER
# ==================================================

def env_str(key, default=""):
    return os.getenv(key, default)



def env_int(key, default=0):
    try:
        return int(os.getenv(key, default))
    except:
        return default



def env_float(key, default=0.0):
    try:
        return float(os.getenv(key, default))
    except:
        return default



def env_bool(key, default=False):

    value = str(
        os.getenv(
            key,
            default
        )
    ).lower()

    return value in (
        "true",
        "1",
        "yes",
        "on"
    )



# ==================================================
# BYBIT API
# ==================================================

BYBIT_API_KEY = env_str(
    "BYBIT_API_KEY"
)


BYBIT_API_SECRET = env_str(
    "BYBIT_API_SECRET"
)


BYBIT_BASE_URL = env_str(
    "BYBIT_BASE_URL",
    "https://api-demo.bybit.com"
)



BYBIT_TESTNET = env_bool(
    "BYBIT_TESTNET",
    False
)


BYBIT_DEMO = env_bool(
    "BYBIT_DEMO",
    True
)



# ==================================================
# MODE
# ==================================================

LIVE_TRADING = env_bool(
    "LIVE_TRADING",
    False
)



# ==================================================
# WEBSOCKET
# ==================================================

BYBIT_PUBLIC_WS = env_str(
    "BYBIT_PUBLIC_WS",
    "wss://stream.bybit.com/v5/public"
)


BYBIT_PRIVATE_WS = env_str(
    "BYBIT_PRIVATE_WS",
    "wss://stream-demo.bybit.com/v5/private"
)



# ==================================================
# ACCOUNT
# ==================================================

ACCOUNT_TYPE = env_str(
    "ACCOUNT_TYPE",
    "UNIFIED"
)


CATEGORY = env_str(
    "CATEGORY",
    "linear"
)



# ==================================================
# SYMBOL
# ==================================================

DEFAULT_SYMBOL = env_str(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



# ==================================================
# ORDER
# ==================================================

DEFAULT_QTY = env_float(
    "DEFAULT_QTY",
    0.001
)


ORDER_TYPE = env_str(
    "ORDER_TYPE",
    "Market"
)


TIME_IN_FORCE = env_str(
    "TIME_IN_FORCE",
    "GTC"
)


ORDER_COOLDOWN = env_int(
    "ORDER_COOLDOWN",
    60
)


ORDER_RETRY = env_int(
    "ORDER_RETRY",
    3
)



# ==================================================
# LEVERAGE
# ==================================================

LEVERAGE = env_int(
    "LEVERAGE",
    3
)



# ==================================================
# RISK MANAGEMENT
# ==================================================

MAX_POSITION_SIZE = env_float(
    "MAX_POSITION_SIZE",
    0.001
)


MAX_DAILY_LOSS_PERCENT = env_float(
    "MAX_DAILY_LOSS_PERCENT",
    5
)


MAX_DRAWDOWN_PERCENT = env_float(
    "MAX_DRAWDOWN_PERCENT",
    15
)


RISK_PER_TRADE_PERCENT = env_float(
    "RISK_PER_TRADE_PERCENT",
    1
)


MAX_LOSS_STREAK = env_int(
    "MAX_LOSS_STREAK",
    5
)



# ==================================================
# TP / SL
# ==================================================

TAKE_PROFIT_PERCENT = env_float(
    "TAKE_PROFIT_PERCENT",
    1
)


STOP_LOSS_PERCENT = env_float(
    "STOP_LOSS_PERCENT",
    0.5
)



# ==================================================
# INDICATORS
# ==================================================

VWAP_LENGTH = env_int(
    "VWAP_LENGTH",
    20
)


SUPERTREND_PERIOD = env_int(
    "SUPERTREND_PERIOD",
    10
)


SUPERTREND_MULTIPLIER = env_float(
    "SUPERTREND_MULTIPLIER",
    3
)


ATR_PERIOD = env_int(
    "ATR_PERIOD",
    14
)



# ==================================================
# WATCHDOG
# ==================================================

WATCHDOG_INTERVAL = env_int(
    "WATCHDOG_INTERVAL",
    30
)


MAX_API_ERROR = env_int(
    "MAX_API_ERROR",
    5
)



# ==================================================
# DATABASE
# ==================================================

DATABASE_PATH = env_str(
    "DATABASE_PATH",
    "data/bot.db"
)



# ==================================================
# TELEGRAM
# ==================================================

TELEGRAM_ENABLED = env_bool(
    "TELEGRAM_ENABLED",
    False
)


TELEGRAM_TOKEN = env_str(
    "TELEGRAM_TOKEN"
)


TELEGRAM_CHAT_ID = env_str(
    "TELEGRAM_CHAT_ID"
)



# ==================================================
# LOG
# ==================================================

LOG_LEVEL = env_str(
    "LOG_LEVEL",
    "INFO"
)



# ==================================================
# VALIDATION
# ==================================================

def validate_config():

    errors = []


    if not BYBIT_API_KEY:

        errors.append(
            "BYBIT_API_KEY missing"
        )


    if not BYBIT_API_SECRET:

        errors.append(
            "BYBIT_API_SECRET missing"
        )


    if CATEGORY not in (
        "linear",
        "inverse",
        "spot"
    ):

        errors.append(
            "Invalid CATEGORY"
        )


    if DEFAULT_QTY <= 0:

        errors.append(
            "DEFAULT_QTY invalid"
        )


    if errors:

        raise Exception(
            "\n".join(errors)
        )



validate_config()



print("==============================")
print("[CONFIG LOADED]")
print("LIVE :", LIVE_TRADING)
print("DEMO :", BYBIT_DEMO)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")

