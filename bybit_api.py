"""
bybit_api.py (V2)
Bybit V5 Real Trading Engine
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
    POSITION_IDX,
    LEVERAGE,
    TRADE_LOG
)

# ======================================
# Logger
# ======================================

logger = logging.getLogger("bybit")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(TRADE_LOG)
    formatter = logging.Formatter("%(asctime)s | %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def log(msg):
    print(msg)
    logger.info(msg)


# ======================================
# Session
# ======================================

session = HTTP(
    testnet=TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)


# ======================================
# Account
# ======================================

def get_balance():
    try:
        return session.get_wallet_balance(accountType="UNIFIED")
    except Exception as e:
        log(f"BALANCE ERROR: {e}")
        return None


# ======================================
# Position
# ======================================

def get_position(symbol=DEFAULT_SYMBOL):

    try:

        res = session.get_positions(
            category=CATEGORY,
            symbol=symbol
        )

        return res["result"]["list"][0]

    except Exception as e:
        log(f"POSITION ERROR: {e}")
        return None


def get_side(symbol=DEFAULT_SYMBOL):

    pos = get_position(symbol)

    if not pos:
        return None

    size = float(pos["size"])

    if size == 0:
        return None

    return "LONG" if pos["side"] == "Buy" else "SHORT"


# ======================================
# Leverage
# ======================================

def set_leverage(symbol=DEFAULT_SYMBOL):

    try:

        session.set_leverage(
            category=CATEGORY,
            symbol=symbol,
            buyLeverage=str(LEVERAGE),
            sellLeverage=str(LEVERAGE)
        )

        log(f"LEVERAGE SET: {LEVERAGE}")

    except Exception as e:
        log(f"LEVERAGE ERROR: {e}")


# ======================================
# Order Core
# ======================================

def order(side, qty, symbol=DEFAULT_SYMBOL, reduce=False):

    try:

        res = session.place_order(
            category=CATEGORY,
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(qty),
            reduceOnly=reduce,
            positionIdx=POSITION_IDX
        )

        log(f"ORDER {side} | {symbol} | {qty}")

        return res

    except Exception as e:
        log(f"ORDER ERROR: {e}")
        return None


# ======================================
# Close Position
# ======================================

def close(symbol=DEFAULT_SYMBOL):

    pos = get_position(symbol)

    if not pos:
        return None

    size = float(pos["size"])

    if size == 0:
        return None

    side = pos["side"]

    close_side = "Sell" if side == "Buy" else "Buy"

    return order(
        close_side,
        size,
        symbol,
        reduce=True
    )


# ======================================
# Trading Actions
# ======================================

def long(symbol=DEFAULT_SYMBOL, qty=ORDER_QTY):

    side = get_side(symbol)

    if side == "LONG":
        log("ALREADY LONG")
        return None

    if side == "SHORT":
        close(symbol)

    return order("Buy", qty, symbol)


def short(symbol=DEFAULT_SYMBOL, qty=ORDER_QTY):

    side = get_side(symbol)

    if side == "SHORT":
        log("ALREADY SHORT")
        return None

    if side == "LONG":
        close(symbol)

    return order("Sell", qty, symbol)


def exit_long(symbol=DEFAULT_SYMBOL):

    if get_side(symbol) != "LONG":
        return None

    return close(symbol)


def exit_short(symbol=DEFAULT_SYMBOL):

    if get_side(symbol) != "SHORT":
        return None

    return close(symbol)


def reverse_long(symbol=DEFAULT_SYMBOL, qty=ORDER_QTY):

    close(symbol)
    return long(symbol, qty)


def reverse_short(symbol=DEFAULT_SYMBOL, qty=ORDER_QTY):

    close(symbol)
    return short(symbol, qty)


# ======================================
# Webhook Executor
# ======================================

def execute(signal, symbol=DEFAULT_SYMBOL, qty=ORDER_QTY):

    signal = signal.upper()

    log(f"SIGNAL: {signal}")

    if signal == "BUY":
        return reverse_long(symbol, qty)

    if signal == "SHORT":
        return reverse_short(symbol, qty)

    if signal == "SELL":
        return exit_long(symbol)

    if signal == "EXIT":
        return exit_short(symbol)

    log(f"UNKNOWN SIGNAL: {signal}")
    return None


# ======================================
# Test
# ======================================

if __name__ == "__main__":

    print("BYBIT API TEST")

    set_leverage()

    print(get_balance())

    print(get_position())
