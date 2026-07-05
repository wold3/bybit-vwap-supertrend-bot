import time
import requests
from pybit.unified_trading import HTTP

from config import *

session = HTTP(
    testnet=TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)


def log(msg):
    print(msg)


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
# TP / SL
# -------------------------

def calc_tp_sl(price, side):

    if side == "LONG":
        tp = price * (1 + TAKE_PROFIT_PCT / 100)
        sl = price * (1 - STOP_LOSS_PCT / 100)
    else:
        tp = price * (1 - TAKE_PROFIT_PCT / 100)
        sl = price * (1 + STOP_LOSS_PCT / 100)

    return tp, sl


# -------------------------
# Order
# -------------------------

def order(side, qty, symbol, reduce=False, tp=None, sl=None):

    try:
        return session.place_order(
            category=CATEGORY,
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(qty),
            reduceOnly=reduce,
            positionIdx=POSITION_IDX,
            takeProfit=tp,
            stopLoss=sl
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
# Telegram
# -------------------------

def notify(msg):

    if TELEGRAM_TOKEN == "":
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    })


# -------------------------
# Trading
# -------------------------

def long(symbol, qty):

    if get_side(symbol) == "LONG":
        return None

    if get_side(symbol) == "SHORT":
        close(symbol)

    entry = order("Buy", qty, symbol)

    price = 0

    try:
        price = float(entry["result"]["price"])
    except:
        pass

    tp, sl = calc_tp_sl(price, "LONG")

    notify(f"LONG {symbol}")

    return entry


def short(symbol, qty):

    if get_side(symbol) == "SHORT":
        return None

    if get_side(symbol) == "LONG":
        close(symbol)

    entry = order("Sell", qty, symbol)

    price = 0

    try:
        price = float(entry["result"]["price"])
    except:
        pass

    tp, sl = calc_tp_sl(price, "SHORT")

    notify(f"SHORT {symbol}")

    return entry


def exit_long(symbol):

    if get_side(symbol) != "LONG":
        return None

    return close(symbol)


def exit_short(symbol):

    if get_side(symbol) != "SHORT":
        return None

    return close(symbol)


# -------------------------
# Execute
# -------------------------

LAST = ""
LAST_TIME = 0


def execute(signal, symbol, qty):

    global LAST, LAST_TIME

    now = time.time()

    if signal == LAST and now - LAST_TIME < 5:
        return None

    LAST = signal
    LAST_TIME = now

    log(f"SIGNAL {signal}")

    if signal == "BUY":
        return long(symbol, qty)

    if signal == "SHORT":
        return short(symbol, qty)

    if signal == "SELL":
        return exit_long(symbol)

    if signal == "EXIT":
        return exit_short(symbol)

    return None
