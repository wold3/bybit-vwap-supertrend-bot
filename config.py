import os
from dotenv import load_dotenv


load_dotenv()


# =====================================
# BYBIT API
# =====================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)


BYBIT_BASE_URL = os.getenv(
    "BYBIT_BASE_URL",
    "https://api.bybit.com"
)



# =====================================
# SYMBOL
# =====================================

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



# =====================================
# WEBSOCKET
# =====================================

BYBIT_WS_URL = os.getenv(
    "BYBIT_WS_URL",
    "wss://stream.bybit.com/v5/public/linear"
)


BYBIT_PRIVATE_WS_URL = os.getenv(
    "BYBIT_PRIVATE_WS_URL",
    "wss://stream.bybit.com/v5/private"
)



# =====================================
# TRADING
# =====================================

LIVE_TRADING = os.getenv(
    "LIVE_TRADING",
    "false"
).lower() == "true"



CATEGORY = os.getenv(
    "CATEGORY",
    "linear"
)



TIMEFRAME = os.getenv(
    "TIMEFRAME",
    "1"
)



# =====================================
# RISK
# =====================================

POSITION_SIZE = float(
    os.getenv(
        "POSITION_SIZE",
        "0.001"
    )
)


LEVERAGE = int(
    os.getenv(
        "LEVERAGE",
        "5"
    )
)



# =====================================
# STRATEGY
# =====================================

ST_LENGTH = int(
    os.getenv(
        "ST_LENGTH",
        "400"
    )
)


ST_MULTIPLIER = float(
    os.getenv(
        "ST_MULTIPLIER",
        "15"
    )
)



# =====================================
# SYSTEM
# =====================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)
