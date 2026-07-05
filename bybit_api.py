import time
import logging
from pybit.unified_trading import HTTP

from config import *

session = HTTP(
    testnet=TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

logger = logging.getLogger("bybit")


def log(msg):
    print(msg)
    logger.info(msg)


# -------------------------
# Position
# -------------------------

def get_position(symbol=DEFAULT_SYMBOL):

    try:
        res = session.get_positions(
            category=CATEGORY,
            symbol=symbol
        )
        return res["result"]["list"][0]
    except:
        return None


def get_side(symbol=DEFAULT_SYMBOL):

    pos = get_position(symbol)

    if not pos:
        return None

    if float(pos["size"]) == 0:
        return None

    return "LONG" if pos["side"] == "Buy" else "SHORT"


# -------------------------
# Order
# -------------------------

def order(side, qty, symbol, reduce=False):

    try:
        return session.place_order(
            category=CATEGORY,
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(qty),
            reduceOnly=reduce,
            positionIdx=POSITION_IDX
        )
    except Exception as e:
        log(e)
        return None


# -------------------------
# Close
# -------------------------

def close(symbol):

    pos = get_position(symbol)

    if not pos:
        return None

    size = float(pos["size"])

    if size == 0:
        return None

    side = pos["side"]

    close_side = "Sell" if side == "Buy" else "Buy"

    return order(close_side, size, symbol, reduce=True)


# -------------------------
# Trading
# -------------------------

def long(symbol, qty):

    if get_side(symbol) == "LONG":
        return None

    if get_side(symbol) == "SHORT":
        close(symbol)

    return order("Buy", qty, symbol)


def short(symbol, qty):

    if get_side(symbol) == "SHORT":
        return None

    if get_side(symbol) == "LONG":
        close(symbol)

    return order("Sell", qty, symbol)


def exit_long(symbol):

    if get_side(symbol) != "LONG":
        return None

    return close(symbol)


def exit_short(symbol):

    if get_side(symbol) != "SHORT":
        return None

    return close(symbol)


# -------------------------
# Risk (basic)
# -------------------------

DAILY_PNL = 0


def risk_ok():

    global DAILY_PNL

    return DAILY_PNL > -MAX_DAILY_LOSS


# -------------------------
# Execute
# -------------------------

LAST = ""
LAST_TIME = 0


def execute(signal, symbol, qty):

    global LAST, LAST_TIME

    if not risk_ok():
        log("DAILY LOSS LIMIT")
        return None

    now = time.time()

    if signal == LAST and now - LAST_TIME < 5:
        return None

    LAST = signal
    LAST_TIME = now

    log(f"SIGNAL: {signal}")

    if signal == "BUY":
        return long(symbol, qty)

    if signal == "SHORT":
        return short(symbol, qty)

    if signal == "SELL":
        return exit_long(symbol)

    if signal == "EXIT":
        return exit_short(symbol)

    return None
