# ==================================================
# CONFIGURATION
# ==================================================

import os

from dotenv import load_dotenv


load_dotenv()



# ==================================================
# HELPER
# ==================================================

def get_bool(
    key,
    default=False
):

    value = os.getenv(
        key,
        str(default)
    )

    return value.lower() in (
        "true",
        "1",
        "yes"
    )



def get_int(
    key,
    default=0
):

    try:

        return int(
            os.getenv(
                key,
                default
            )
        )

    except:

        return default



def get_float(
    key,
    default=0.0
):

    try:

        return float(
            os.getenv(
                key,
                default
            )
        )

    except:

        return default



def get_str(
    key,
    default=""
):

    return os.getenv(
        key,
        default
    )



# ==================================================
# BYBIT API
# ==================================================

BYBIT_API_KEY = get_str(
    "BYBIT_API_KEY"
)


BYBIT_API_SECRET = get_str(
    "BYBIT_API_SECRET"
)



# ==================================================
# MODE
# ==================================================

BYBIT_TESTNET = get_bool(
    "BYBIT_TESTNET"
)


BYBIT_DEMO = get_bool(
    "BYBIT_DEMO"
)


LIVE_TRADING = get_bool(
    "LIVE_TRADING"
)



# ==================================================
# SERVER
# ==================================================

BYBIT_BASE_URL = get_str(
    "BYBIT_BASE_URL",
    "https://api-demo.bybit.com"
)



# ==================================================
# WEBSOCKET
# ==================================================

BYBIT_PUBLIC_WS = get_str(
    "BYBIT_PUBLIC_WS"
)


BYBIT_PRIVATE_WS = get_str(
    "BYBIT_PRIVATE_WS"
)



# ==================================================
# ACCOUNT
# ==================================================

ACCOUNT_TYPE = get_str(
    "ACCOUNT_TYPE",
    "UNIFIED"
)


CATEGORY = get_str(
    "CATEGORY",
    "linear"
)



# ==================================================
# SYMBOL
# ==================================================

DEFAULT_SYMBOL = get_str(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



# ==================================================
# ORDER
# ==================================================

DEFAULT_QTY = get_float(
    "DEFAULT_QTY",
    0.001
)


ORDER_TYPE = get_str(
    "ORDER_TYPE",
    "Market"
)


TIME_IN_FORCE = get_str(
    "TIME_IN_FORCE",
    "GTC"
)


ORDER_COOLDOWN = get_int(
    "ORDER_COOLDOWN",
    60
)


ORDER_RETRY = get_int(
    "ORDER_RETRY",
    3
)



# ==================================================
# LEVERAGE
# ==================================================

LEVERAGE = get_int(
    "LEVERAGE",
    3
)



# ==================================================
# RISK
# ==================================================

MAX_POSITION_SIZE = get_float(
    "MAX_POSITION_SIZE",
    0.001
)


MAX_DAILY_LOSS_PERCENT = get_float(
    "MAX_DAILY_LOSS_PERCENT",
    5
)


MAX_DRAWDOWN_PERCENT = get_float(
    "MAX_DRAWDOWN_PERCENT",
    15
)


MAX_LOSS_STREAK = get_int(
    "MAX_LOSS_STREAK",
    5
)


RISK_PER_TRADE_PERCENT = get_float(
    "RISK_PER_TRADE_PERCENT",
    1
)



# ==================================================
# TP / SL
# ==================================================

TAKE_PROFIT_PERCENT = get_float(
    "TAKE_PROFIT_PERCENT",
    1
)


STOP_LOSS_PERCENT = get_float(
    "STOP_LOSS_PERCENT",
    0.5
)



# ==================================================
# INDICATORS
# ==================================================

VWAP_LENGTH = get_int(
    "VWAP_LENGTH",
    20
)


SUPERTREND_PERIOD = get_int(
    "SUPERTREND_PERIOD",
    10
)


SUPERTREND_MULTIPLIER = get_float(
    "SUPERTREND_MULTIPLIER",
    3
)


ATR_PERIOD = get_int(
    "ATR_PERIOD",
    14
)



# ==================================================
# WATCHDOG
# ==================================================

WATCHDOG_INTERVAL = get_int(
    "WATCHDOG_INTERVAL",
    30
)


MAX_API_ERROR = get_int(
    "MAX_API_ERROR",
    5
)



# ==================================================
# DATABASE
# ==================================================

DATABASE_PATH = get_str(
    "DATABASE_PATH",
    "data/bot.db"
)



# ==================================================
# TELEGRAM
# ==================================================

TELEGRAM_ENABLED = get_bool(
    "TELEGRAM_ENABLED"
)


TELEGRAM_TOKEN = get_str(
    "TELEGRAM_TOKEN"
)


TELEGRAM_CHAT_ID = get_str(
    "TELEGRAM_CHAT_ID"
)



# ==================================================
# LOG
# ==================================================

LOG_LEVEL = get_str(
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
            "Missing BYBIT_API_KEY"
        )


    if not BYBIT_API_SECRET:

        errors.append(
            "Missing BYBIT_API_SECRET"
        )



    if CATEGORY not in (
        "linear",
        "spot",
        "inverse"
    ):

        errors.append(
            "Invalid CATEGORY"
        )



    if errors:

        raise Exception(
            "\n".join(errors)
        )



# 실행 시 설정 검사

validate_config()



print("==============================")
print("[CONFIG LOADED]")
print("MODE :", 
      "LIVE" if LIVE_TRADING else "TEST")
print("DEMO :", BYBIT_DEMO)
print("CATEGORY :", CATEGORY)
print("SYMBOL :", DEFAULT_SYMBOL)
print("==============================")
