"""
bybit_api.py

Bybit V5 Trading Engine
"""

import logging
from pybit.unified_trading import HTTP

from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    TESTNET,
    CATEGORY,
    DEFAULT_SYMBOL,
    ORDER_QTY,
    ACCOUNT_TYPE,
    LOG_FILE
)

# -----------------------------------
# Logging
# -----------------------------------

logger = logging.getLogger("bybit")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

# -----------------------------------
# Session
# -----------------------------------

session = HTTP(
    testnet=TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

# -----------------------------------
# Helpers
# -----------------------------------

def log(msg):
    print(msg)
    logger.info(msg)

# -----------------------------------
# Account
# -----------------------------------

def get_wallet_balance():
    """
    계좌 잔고 조회
    """

    try:

        result = session.get_wallet_balance(
            accountType=ACCOUNT_TYPE
        )

        return result

    except Exception as e:

        log(f"BALANCE ERROR : {e}")

        return None

# -----------------------------------
# Position
# -----------------------------------

def get_position(symbol=DEFAULT_SYMBOL):

    try:

        result = session.get_positions(
            category=CATEGORY,
            symbol=symbol
        )

        if "result" not in result:
            return None

        positions = result["result"]["list"]

        if len(positions) == 0:
            return None

        return positions[0]

    except Exception as e:

        log(f"POSITION ERROR : {e}")

        return None

# -----------------------------------
# Current Side
# -----------------------------------

def get_position_side(symbol=DEFAULT_SYMBOL):

    pos = get_position(symbol)

    if pos is None:
        return None

    size = float(pos["size"])

    if size == 0:
        return None

    side = pos["side"]

    if side == "Buy":
        return "LONG"

    if side == "Sell":
        return "SHORT"

    return None

# -----------------------------------
# Order
# -----------------------------------

def market_order(
    side,
    qty=ORDER_QTY,
    symbol=DEFAULT_SYMBOL,
    reduce_only=False
):

    try:

        result = session.place_order(
            category=CATEGORY,
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            reduceOnly=reduce_only
        )

        log(
            f"ORDER SUCCESS | "
            f"{side} | "
            f"{qty} | "
            f"{symbol}"
        )

        return result

    except Exception as e:

        log(f"ORDER ERROR : {e}")

        return None

# -----------------------------------
# Close Position
# -----------------------------------

def close_position(symbol=DEFAULT_SYMBOL):

    try:

        pos = get_position(symbol)

        if pos is None:
            log("NO POSITION")

            return

        size = float(pos["size"])

        if size <= 0:
            log("POSITION SIZE = 0")

            return

        side = pos["side"]

        close_side = "Sell"

        if side == "Sell":
            close_side = "Buy"

        result = market_order(
            side=close_side,
            qty=size,
            symbol=symbol,
            reduce_only=True
        )

        log(
            f"CLOSE POSITION | "
            f"{symbol} | "
            f"{size}"
        )

        return result

    except Exception as e:

        log(f"CLOSE ERROR : {e}")

        return None
