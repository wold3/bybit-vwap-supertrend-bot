import os
from dotenv import load_dotenv


load_dotenv()



# =====================================================
# BYBIT
# =====================================================


BYBIT_TESTNET = (
    os.getenv(
        "BYBIT_TESTNET",
        "True"
    )
    == "True"
)


LIVE_TRADING = (
    os.getenv(
        "LIVE_TRADING",
        "False"
    )
    == "True"
)



BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)



# =====================================================
# REST URL
# =====================================================


if BYBIT_TESTNET:

    # Testnet
    BYBIT_BASE_URL = (
        "https://api-testnet.bybit.com"
    )

else:

    # Mainnet
    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )



# =====================================================
# WEBSOCKET URL
# =====================================================


if BYBIT_TESTNET:


    # Testnet Public Linear

    BYBIT_PUBLIC_WS = (
        "wss://stream-testnet.bybit.com/v5/public/linear"
    )


    # Testnet Private

    BYBIT_PRIVATE_WS = (
        "wss://stream-testnet.bybit.com/v5/private"
    )



else:


    # Mainnet Public Linear

    BYBIT_PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public/linear"
    )


    # Mainnet Private

    BYBIT_PRIVATE_WS = (
        "wss://stream.bybit.com/v5/private"
    )





# =====================================================
# TRADING
# =====================================================


DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)



DEFAULT_INTERVAL = (
    "1"
)



DEFAULT_QTY = float(
    os.getenv(
        "DEFAULT_QTY",
        "0.001"
    )
)



# =====================================================
# RISK
# =====================================================


MAX_POSITION_SIZE = float(
    os.getenv(
        "MAX_POSITION_SIZE",
        "0.01"
    )
)



DAILY_LOSS_LIMIT = float(
    os.getenv(
        "DAILY_LOSS_LIMIT",
        "-100"
    )
)



ORDER_COOLDOWN = int(
    os.getenv(
        "ORDER_COOLDOWN",
        "30"
    )
)



# =====================================================
# SYSTEM
# =====================================================


LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)



print("==============================")
print("[CONFIG LOADED]")
print("TESTNET :", BYBIT_TESTNET)
print("LIVE :", LIVE_TRADING)
print("SYMBOL :", DEFAULT_SYMBOL)
print("REST :", BYBIT_BASE_URL)
print("PUBLIC WS :", BYBIT_PUBLIC_WS)
print("==============================")
